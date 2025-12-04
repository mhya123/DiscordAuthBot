from __future__ import annotations

import os
import logging
from typing import Optional

import discord
from discord import app_commands, Interaction
from discord.ext import commands

from .auth_api import AuthAPI
from .i18n import t
from .prefs import set_lang, get_lang
from .storage import mark_verified, revoke_verified, is_verified, get_user_info

log = logging.getLogger("authbot.auth_commands")


def _truthy(val: Optional[str], default: bool = True) -> bool:
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "y", "on"}


def get_role_name() -> str:
    return os.getenv("AUTH_SUCCESS_ROLE", "Verified")


def get_channel_name() -> str:
    return os.getenv("AUTH_CHANNEL_NAME", "auth-verify")


# ==================== 辅助函数 ====================

async def grant_role_and_nick(interaction: Interaction, username: str, role_name: str) -> Optional[str]:
    """授予角色和更新昵称"""
    guild = interaction.guild
    if guild is None:
        return t("guild_not_found", get_lang(0, interaction.user.id))
    
    member = guild.get_member(interaction.user.id) or await guild.fetch_member(interaction.user.id)
    role = discord.utils.get(guild.roles, name=role_name)
    
    if role is None:
        try:
            role = await guild.create_role(name=role_name, reason="Auth success: create missing role")
        except Exception:
            return t("role_create_failed", get_lang(guild.id, interaction.user.id))

    try:
        await member.add_roles(role, reason=f"Authenticated as {username}")
    except discord.Forbidden:
        return t("role_permission_denied", get_lang(guild.id, interaction.user.id))
    except Exception as e:
        return t("role_assign_failed", get_lang(guild.id, interaction.user.id), error=str(e))

    try:
        await member.edit(nick=username, reason="Set nickname after authentication")
    except discord.Forbidden:
        pass
    except Exception:
        pass
    return None


def create_login_modal(guild: discord.Guild, interaction: Interaction, api: AuthAPI, bot: Optional[commands.Bot] = None):
    """创建登录模态框"""
    
    class LoginModal(discord.ui.Modal):
        def __init__(self):
            super().__init__(title=t("modal_title", get_lang(guild.id, interaction.user.id)))
        
        login_input: discord.ui.TextInput = discord.ui.TextInput(
            label=t("modal_login_label", get_lang(guild.id, interaction.user.id)), 
            placeholder=t("modal_login_placeholder", get_lang(guild.id, interaction.user.id)), 
            required=True, 
            max_length=120
        )
        password_input: discord.ui.TextInput = discord.ui.TextInput(
            label=t("modal_password_label", get_lang(guild.id, interaction.user.id)), 
            style=discord.TextStyle.short, 
            required=True, 
            max_length=120
        )

        async def on_submit(self, modal_interaction: Interaction) -> None:
            await modal_interaction.response.defer(ephemeral=True, thinking=True)
            role_name = get_role_name()
            
            try:
                payload = await api.login(login=str(self.login_input.value), password=str(self.password_input.value))
            except Exception as e:
                log.exception("Auth request failed: user=%s", modal_interaction.user.id)
                await modal_interaction.followup.send(
                    t("auth_request_failed", get_lang(guild.id, modal_interaction.user.id), error=str(e)), 
                    ephemeral=True
                )
                return

            if not AuthAPI.is_success(payload):
                status = int(payload.get("status_code", 0))
                log.info("Auth failed: user=%s http_status=%s", modal_interaction.user.id, status)
                if status == 500:
                    await modal_interaction.followup.send(
                        t("auth_failed_500", get_lang(guild.id, modal_interaction.user.id)), 
                        ephemeral=True
                    )
                else:
                    await modal_interaction.followup.send(
                        t("auth_failed_generic", get_lang(guild.id, modal_interaction.user.id)), 
                        ephemeral=True
                    )
                return

            username = AuthAPI.pick_username(payload) or "user"
            log.info("Auth success: user=%s username=%s", modal_interaction.user.id, username)
            
            err = await grant_role_and_nick(modal_interaction, username, role_name)
            if err:
                log.warning("Post-auth issue: user=%s err=%s", modal_interaction.user.id, err)
                await modal_interaction.followup.send(
                    t("auth_partial_success", get_lang(guild.id, modal_interaction.user.id), username=username, error=err), 
                    ephemeral=True
                )
                return

            try:
                mark_verified(
                    guild_id=guild.id, 
                    user_id=modal_interaction.user.id, 
                    record={"username": username}
                )
            except Exception:
                pass

            await modal_interaction.followup.send(
                t("auth_success", get_lang(guild.id, modal_interaction.user.id), username=username), 
                ephemeral=True
            )

    return LoginModal()


# ==================== 管理员命令组 ====================

class AuthCommands(app_commands.Group, name="auth", description="🛡️ 身份验证管理 / Auth management (Admin)"):
    """管理员命令组 - 用于设置和管理验证系统"""
    
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    async def _ensure_channel_overwrites(self, channel: discord.TextChannel, guild: discord.Guild, success_role: discord.Role) -> None:
        await channel.set_permissions(guild.default_role, view_channel=True, send_messages=True)
        await channel.set_permissions(success_role, view_channel=True, send_messages=True)
        await channel.set_permissions(guild.me, view_channel=True, send_messages=True)

    @app_commands.command(name="setup", description="🔧 初始化认证系统 / Initialize auth system")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(self, interaction: Interaction):
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(t("must_use_in_server", get_lang(0, interaction.user.id)), ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True, thinking=True)

        role_name = get_role_name()
        channel_name = get_channel_name()

        # Create/find roles
        role = discord.utils.get(guild.roles, name=role_name)
        if role is None:
            log.info("Creating role '%s' in guild %s", role_name, guild.id)
            role = await guild.create_role(name=role_name, reason="Auth setup: success role")

        # Create/find text channel
        channel = discord.utils.get(guild.text_channels, name=channel_name)
        if channel is None:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                role: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            }
            log.info("Creating auth channel '%s' in guild %s", channel_name, guild.id)
            channel = await guild.create_text_channel(channel_name, overwrites=overwrites, reason="Auth setup: channel")
        else:
            log.info("Updating auth channel '%s' overwrites in guild %s", channel.name, guild.id)
            await self._ensure_channel_overwrites(channel, guild, role)

        # Hide other channels from @everyone, allow Verified
        hide_others = _truthy(os.getenv("AUTH_HIDE_OTHER_CHANNELS", "true"), default=True)
        if hide_others:
            for category in guild.categories:
                try:
                    await category.set_permissions(guild.default_role, view_channel=False)
                    await category.set_permissions(role, view_channel=True)
                except Exception as e:
                    log.warning("Failed to set category overwrite: category=%s err=%s", category.id, e)
            for ch in guild.text_channels:
                if ch.id == channel.id:
                    continue
                try:
                    await ch.set_permissions(guild.default_role, view_channel=False)
                    await ch.set_permissions(role, view_channel=True, send_messages=True)
                except Exception as e:
                    log.warning("Failed to set channel overwrite: channel=%s err=%s", ch.id, e)

        await interaction.followup.send(
            t("setup_complete", get_lang(guild.id, interaction.user.id), role=role.mention, channel=channel.mention), 
            ephemeral=True
        )

        # Post welcome message with language selection and quick login
        await self._post_welcome_message(channel, guild)

    async def _post_welcome_message(self, channel: discord.TextChannel, guild: discord.Guild):
        """发送欢迎消息和快捷操作按钮"""
        bot = self.bot
        
        class WelcomeView(discord.ui.View):
            def __init__(self) -> None:
                super().__init__(timeout=None)

            @discord.ui.button(label="🔐 登录验证 / Login", style=discord.ButtonStyle.success, custom_id="quick_login", row=0)
            async def quick_login(self, btn_interaction: Interaction, button: discord.ui.Button):
                # Check if already verified
                member = guild.get_member(btn_interaction.user.id)
                if member:
                    role = discord.utils.get(guild.roles, name=get_role_name())
                    if role and role in member.roles:
                        await btn_interaction.response.send_message(
                            t("already_verified", get_lang(guild.id, btn_interaction.user.id)), 
                            ephemeral=True
                        )
                        return

                base = os.getenv("AUTH_API_BASE")
                if not base:
                    await btn_interaction.response.send_message(
                        t("api_not_config", get_lang(guild.id, btn_interaction.user.id)), 
                        ephemeral=True
                    )
                    return

                api = AuthAPI(base)
                modal = create_login_modal(guild, btn_interaction, api)
                await btn_interaction.response.send_modal(modal)

            @discord.ui.button(label="🇨🇳 中文", style=discord.ButtonStyle.secondary, custom_id="lang_zh", row=1)
            async def zh(self, btn_interaction: Interaction, button: discord.ui.Button):
                set_lang(guild.id, btn_interaction.user.id, "zh")
                await btn_interaction.response.send_message(t("lang_set_zh", "zh"), ephemeral=True)

            @discord.ui.button(label="🇺🇸 English", style=discord.ButtonStyle.secondary, custom_id="lang_en", row=1)
            async def en(self, btn_interaction: Interaction, button: discord.ui.Button):
                set_lang(guild.id, btn_interaction.user.id, "en")
                await btn_interaction.response.send_message(t("lang_set_en", "en"), ephemeral=True)

        embed = discord.Embed(
            title="🔐 身份验证 / Authentication",
            description=t("welcome_message", "zh"),
            color=discord.Color.blue()
        )
        embed.add_field(
            name="📋 使用说明 / Instructions",
            value=t("welcome_instructions", "zh"),
            inline=False
        )
        embed.set_footer(text="AuthBot • 点击按钮开始验证")

        try:
            await channel.send(embed=embed, view=WelcomeView())
        except Exception as e:
            log.warning("Failed to send welcome message: %s", e)

    @setup.error
    async def setup_error(self, interaction: Interaction, error: Exception):
        from discord.app_commands.errors import MissingPermissions
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(
                t("missing_admin", get_lang(interaction.guild.id if interaction.guild else 0, interaction.user.id)), 
                ephemeral=True
            )
        else:
            if interaction.response.is_done():
                await interaction.followup.send(
                    t("generic_error", get_lang(interaction.guild.id if interaction.guild else 0, interaction.user.id)), 
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    t("generic_error", get_lang(interaction.guild.id if interaction.guild else 0, interaction.user.id)), 
                    ephemeral=True
                )

    @app_commands.command(name="revoke", description="🚫 撤销用户验证 / Revoke verification")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(member="要撤销的成员 / Member to revoke")
    async def revoke(self, interaction: Interaction, member: discord.Member):
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(t("must_use_in_server", get_lang(0, interaction.user.id)), ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True, thinking=True)

        role_name = get_role_name()
        role = discord.utils.get(guild.roles, name=role_name)
        removed_role = False
        if role and role in member.roles:
            try:
                await member.remove_roles(role, reason="Verification revoked by admin")
                removed_role = True
            except Exception:
                pass

        removed_db = revoke_verified(guild.id, member.id)

        msg = t("revoke_success", get_lang(guild.id, interaction.user.id), member=member.mention)
        if removed_role:
            msg += t("revoke_role_removed", get_lang(guild.id, interaction.user.id))
        if removed_db:
            msg += t("revoke_record_cleared", get_lang(guild.id, interaction.user.id))

        await interaction.followup.send(msg, ephemeral=True)

    @revoke.error
    async def revoke_error(self, interaction: Interaction, error: Exception):
        from discord.app_commands.errors import MissingPermissions
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(
                t("missing_admin", get_lang(interaction.guild.id if interaction.guild else 0, interaction.user.id)), 
                ephemeral=True
            )
        else:
            if interaction.response.is_done():
                await interaction.followup.send(
                    t("generic_error", get_lang(interaction.guild.id if interaction.guild else 0, interaction.user.id)), 
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    t("generic_error", get_lang(interaction.guild.id if interaction.guild else 0, interaction.user.id)), 
                    ephemeral=True
                )

    @app_commands.command(name="list", description="📋 查看已验证用户 / List verified users")
    @app_commands.checks.has_permissions(administrator=True)
    async def list_verified(self, interaction: Interaction):
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(t("must_use_in_server", get_lang(0, interaction.user.id)), ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        
        from .storage import load_db
        db = load_db()
        verified = db.get("guilds", {}).get(str(guild.id), {}).get("verified", {})
        
        if not verified:
            await interaction.followup.send(t("no_verified_users", get_lang(guild.id, interaction.user.id)), ephemeral=True)
            return

        lines = []
        for user_id, info in verified.items():
            username = info.get("username", "Unknown")
            member = guild.get_member(int(user_id))
            if member:
                lines.append(f"• {member.mention} → `{username}`")
            else:
                lines.append(f"• <@{user_id}> → `{username}` (已离开)")
        
        embed = discord.Embed(
            title=t("verified_list_title", get_lang(guild.id, interaction.user.id)),
            description="\n".join(lines[:25]),
            color=discord.Color.green()
        )
        if len(verified) > 25:
            embed.set_footer(text=f"显示 25/{len(verified)} 条记录")
        
        await interaction.followup.send(embed=embed, ephemeral=True)

    @list_verified.error
    async def list_verified_error(self, interaction: Interaction, error: Exception):
        from discord.app_commands.errors import MissingPermissions
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(
                t("missing_admin", get_lang(interaction.guild.id if interaction.guild else 0, interaction.user.id)), 
                ephemeral=True
            )


# ==================== 顶级斜杠命令（用户常用） ====================

@app_commands.command(name="login", description="🔐 登录验证账号 / Login to verify")
async def login_command(interaction: Interaction):
    """直接登录命令 - 用户最常用的命令"""
    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message(t("must_use_in_server", get_lang(0, interaction.user.id)), ephemeral=True)
        return

    # Channel restriction check
    restrict = _truthy(os.getenv("AUTH_LOGIN_CHANNEL_ONLY", "true"), default=True)
    expected_channel = get_channel_name()
    if restrict:
        if not isinstance(interaction.channel, discord.TextChannel) or interaction.channel.name != expected_channel:
            log.info("Login rejected: user=%s channel=%s expected=%s", interaction.user.id, getattr(interaction.channel, 'name', '?'), expected_channel)
            await interaction.response.send_message(
                t("use_channel", get_lang(guild.id, interaction.user.id), channel=expected_channel), 
                ephemeral=True
            )
            return

    # Check if already verified
    role_name = get_role_name()
    member = guild.get_member(interaction.user.id) or await guild.fetch_member(interaction.user.id)
    verified_role = discord.utils.get(guild.roles, name=role_name)
    if (verified_role and verified_role in member.roles) or is_verified(guild.id, member.id):
        await interaction.response.send_message(t("already_verified", get_lang(guild.id, interaction.user.id)), ephemeral=True)
        return

    base = os.getenv("AUTH_API_BASE")
    if not base:
        await interaction.response.send_message(t("api_not_config", get_lang(guild.id, interaction.user.id)), ephemeral=True)
        return

    api = AuthAPI(base)
    modal = create_login_modal(guild, interaction, api)
    await interaction.response.send_modal(modal)


@app_commands.command(name="status", description="📊 查看验证状态 / Check verification status")
async def status_command(interaction: Interaction):
    """查看当前用户的验证状态"""
    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message(t("must_use_in_server", get_lang(0, interaction.user.id)), ephemeral=True)
        return

    member = guild.get_member(interaction.user.id)
    role_name = get_role_name()
    role = discord.utils.get(guild.roles, name=role_name)
    
    has_role = role and member and role in member.roles
    user_info = get_user_info(guild.id, interaction.user.id)
    
    lang = get_lang(guild.id, interaction.user.id)
    
    if has_role or user_info:
        username = user_info.get("username", "Unknown") if user_info else "Unknown"
        embed = discord.Embed(
            title="✅ " + t("status_verified_title", lang),
            description=t("status_verified_desc", lang, username=username),
            color=discord.Color.green()
        )
        if has_role and role:
            embed.add_field(name=t("status_role", lang), value=role.mention, inline=True)
    else:
        embed = discord.Embed(
            title="❌ " + t("status_unverified_title", lang),
            description=t("status_unverified_desc", lang),
            color=discord.Color.red()
        )
        embed.add_field(
            name=t("status_how_to", lang), 
            value=t("status_how_to_desc", lang), 
            inline=False
        )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)


@app_commands.command(name="lang", description="🌐 切换显示语言 / Switch language")
@app_commands.describe(language="选择语言 / Choose language")
@app_commands.choices(language=[
    app_commands.Choice(name="🇨🇳 中文", value="zh"),
    app_commands.Choice(name="🇺🇸 English", value="en"),
])
async def lang_command(interaction: Interaction, language: app_commands.Choice[str]):
    """快捷语言切换命令"""
    guild_id = interaction.guild.id if interaction.guild else 0
    set_lang(guild_id, interaction.user.id, language.value)
    
    if language.value == "zh":
        await interaction.response.send_message(t("lang_set_zh", "zh"), ephemeral=True)
    else:
        await interaction.response.send_message(t("lang_set_en", "en"), ephemeral=True)


@app_commands.command(name="help", description="❓ 显示帮助信息 / Show help")
async def help_command(interaction: Interaction):
    """显示完整的帮助信息"""
    guild_id = interaction.guild.id if interaction.guild else 0
    lang = get_lang(guild_id, interaction.user.id)
    
    embed = discord.Embed(
        title="🤖 AuthBot " + t("help_title", lang),
        description=t("help_description", lang),
        color=discord.Color.blue()
    )
    
    # User commands
    embed.add_field(
        name="👤 " + t("help_user_commands", lang),
        value=(
            "`/login` - " + t("help_login_desc", lang) + "\n"
            "`/status` - " + t("help_status_desc", lang) + "\n"
            "`/lang` - " + t("help_lang_desc", lang) + "\n"
            "`/help` - " + t("help_help_desc", lang)
        ),
        inline=False
    )
    
    # Admin commands
    embed.add_field(
        name="🛡️ " + t("help_admin_commands", lang),
        value=(
            "`/auth setup` - " + t("help_setup_desc", lang) + "\n"
            "`/auth revoke` - " + t("help_revoke_desc", lang) + "\n"
            "`/auth list` - " + t("help_list_desc", lang)
        ),
        inline=False
    )
    
    embed.set_footer(text="AuthBot v1.0 • github.com/mhya123/DiscordAuthBot")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)


def register_commands(bot: commands.Bot) -> None:
    """注册所有命令到 bot"""
    # 顶级命令（用户常用）
    bot.tree.add_command(login_command)
    bot.tree.add_command(status_command)
    bot.tree.add_command(lang_command)
    bot.tree.add_command(help_command)
    # 管理员命令组
    bot.tree.add_command(AuthCommands(bot))
