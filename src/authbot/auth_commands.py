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
from .storage import mark_verified, revoke_verified, is_verified

log = logging.getLogger("authbot.auth_commands")


def _truthy(val: Optional[str], default: bool = True) -> bool:
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "y", "on"}


class AuthCommands(app_commands.Group, name="auth", description="Account authentication"):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    async def _ensure_channel_overwrites(self, channel: discord.TextChannel, guild: discord.Guild, success_role: discord.Role) -> None:
        # Auth channel: everyone can see and speak; success role can also speak; bot can speak
        await channel.set_permissions(guild.default_role, view_channel=True, send_messages=True)
        await channel.set_permissions(success_role, view_channel=True, send_messages=True)
        await channel.set_permissions(guild.me, view_channel=True, send_messages=True)

    async def _grant_role_and_nick(self, interaction: Interaction, username: str, role_name: str) -> Optional[str]:
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

        # Assign role
        try:
            await member.add_roles(role, reason=f"Authenticated as {username}")
        except discord.Forbidden:
            return t("role_permission_denied", get_lang(guild.id, interaction.user.id))
        except Exception as e:
            return t("role_assign_failed", get_lang(guild.id, interaction.user.id), error=str(e))

        # Change nickname
        try:
            await member.edit(nick=username, reason="Set nickname after authentication")
        except discord.Forbidden:
            # Not critical: insufficient perms or higher role order
            return None
        except Exception:
            return None
        return None

    @app_commands.command(name="setup", description="Create auth role & channel (admin only)")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(self, interaction: Interaction):
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(t("must_use_in_server", get_lang(0, interaction.user.id)), ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True, thinking=True)

        # Desired names from env
        role_name = os.getenv("AUTH_SUCCESS_ROLE", "Verified")
        unverified_name = os.getenv("AUTH_UNVERIFIED_ROLE", "Unverified")
        channel_name = os.getenv("AUTH_CHANNEL_NAME", "auth-verify")

        # Create/find roles
        role = discord.utils.get(guild.roles, name=role_name)
        if role is None:
            log.info("Creating role '%s' in guild %s", role_name, guild.id)
            role = await guild.create_role(name=role_name, reason="Auth setup: success role")

    # Note: Using @everyone as unverified; 'Unverified' role is optional and not required.

        # Create/find text channel and apply permission template
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
            # Categories first for broad effect
            for category in guild.categories:
                try:
                    await category.set_permissions(guild.default_role, view_channel=False)
                    await category.set_permissions(role, view_channel=True)
                except Exception as e:
                    log.warning("Failed to set category overwrite: category=%s err=%s", category.id, e)
            # Per text channel, skip the auth channel
            for ch in guild.text_channels:
                if ch.id == channel.id:
                    continue
                try:
                    await ch.set_permissions(guild.default_role, view_channel=False)
                    await ch.set_permissions(role, view_channel=True, send_messages=True)
                except Exception as e:
                    log.warning("Failed to set channel overwrite: channel=%s err=%s", ch.id, e)

        await interaction.followup.send(t("setup_complete", get_lang(guild.id, interaction.user.id), role=role.mention, channel=channel.mention), ephemeral=True)

        # Post a language selection message in the auth channel
        class LangView(discord.ui.View):
            def __init__(self) -> None:
                super().__init__(timeout=None)

            @discord.ui.button(label="中文", style=discord.ButtonStyle.primary, custom_id="lang_zh")
            async def zh(self, btn_interaction: Interaction, button: discord.ui.Button):  # type: ignore[override]
                set_lang(guild.id, btn_interaction.user.id, "zh")
                await btn_interaction.response.send_message(t("lang_set_zh", "zh"), ephemeral=True)

            @discord.ui.button(label="English", style=discord.ButtonStyle.secondary, custom_id="lang_en")
            async def en(self, btn_interaction: Interaction, button: discord.ui.Button):  # type: ignore[override]
                set_lang(guild.id, btn_interaction.user.id, "en")
                await btn_interaction.response.send_message(t("lang_set_en", "en"), ephemeral=True)

        try:
            await channel.send(content=t("lang_prompt", "zh"), view=LangView())
        except Exception:
            pass

    @setup.error
    async def setup_error(self, interaction: Interaction, error: Exception):
        try:
            from discord.app_commands.errors import MissingPermissions
        except Exception:
            MissingPermissions = tuple()  # type: ignore
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(t("missing_admin", get_lang(interaction.guild.id if interaction.guild else 0, interaction.user.id)), ephemeral=True)
        else:
            # Fallback
            if interaction.response.is_done():
                await interaction.followup.send(t("generic_error", get_lang(interaction.guild.id if interaction.guild else 0, interaction.user.id)), ephemeral=True)
            else:
                await interaction.response.send_message(t("generic_error", get_lang(interaction.guild.id if interaction.guild else 0, interaction.user.id)), ephemeral=True)

    @app_commands.command(name="login", description="Open a secure login modal to authenticate")
    async def login(self, interaction: Interaction):
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(t("must_use_in_server", get_lang(0, interaction.user.id)), ephemeral=True)
            return

        # Restrict to specific channel if configured
        restrict = _truthy(os.getenv("AUTH_LOGIN_CHANNEL_ONLY", "true"), default=True)
        expected_channel = os.getenv("AUTH_CHANNEL_NAME", "auth-verify")
        if restrict:
            if not isinstance(interaction.channel, discord.TextChannel) or interaction.channel.name != expected_channel:
                log.info(
                    "Login rejected due to wrong channel: user=%s channel=%s expected=%s",
                    interaction.user.id,
                    getattr(interaction.channel, 'name', '?'),
                    expected_channel,
                )
                await interaction.response.send_message(t("use_channel", get_lang(guild.id, interaction.user.id), channel=expected_channel), ephemeral=True)
                return

        # Prevent verified users from re-auth
        role_name = os.getenv("AUTH_SUCCESS_ROLE", "Verified")
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
                try:
                    payload = await api.login(login=str(self.login_input.value), password=str(self.password_input.value))
                except Exception as e:
                    log.exception("Auth request failed: user=%s", modal_interaction.user.id)
                    await modal_interaction.followup.send(t("auth_request_failed", get_lang(guild.id, modal_interaction.user.id), error=str(e)), ephemeral=True)
                    return

                if not AuthAPI.is_success(payload):
                    status = int(payload.get("status_code", 0))
                    log.info("Auth failed: user=%s http_status=%s", modal_interaction.user.id, status)
                    if status == 500:
                        await modal_interaction.followup.send(t("auth_failed_500", get_lang(guild.id, modal_interaction.user.id)), ephemeral=True)
                    else:
                        await modal_interaction.followup.send(t("auth_failed_generic", get_lang(guild.id, modal_interaction.user.id)), ephemeral=True)
                    return

                username = AuthAPI.pick_username(payload) or "user"
                log.info("Auth success: user=%s username=%s", modal_interaction.user.id, username)
                err = await AuthCommands._grant_role_and_nick(self=outer_self, interaction=modal_interaction, username=username, role_name=role_name)
                if err:
                    log.warning("Post-auth issue: user=%s err=%s", modal_interaction.user.id, err)
                    await modal_interaction.followup.send(t("auth_partial_success", get_lang(guild.id, modal_interaction.user.id), username=username, error=err), ephemeral=True)
                    return
                # Persist verification record
                g = modal_interaction.guild
                try:
                    mark_verified(guild_id=g.id if g else interaction.guild.id, user_id=modal_interaction.user.id, record={"username": username})
                except Exception:
                    pass

                await modal_interaction.followup.send(t("auth_success", get_lang(guild.id, modal_interaction.user.id), username=username), ephemeral=True)

        outer_self = self
        await interaction.response.send_modal(LoginModal())

    @app_commands.command(name="revoke", description="Revoke a member's verified status (admin only)")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(member="Member to revoke")
    async def revoke(self, interaction: Interaction, member: discord.Member):
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(t("must_use_in_server", get_lang(0, interaction.user.id)), ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True, thinking=True)

        role_name = os.getenv("AUTH_SUCCESS_ROLE", "Verified")
        role = discord.utils.get(guild.roles, name=role_name)
        removed_role = False
        if role and role in member.roles:
            try:
                await member.remove_roles(role, reason="Verification revoked by admin")
                removed_role = True
            except Exception:
                pass

        removed_db = revoke_verified(guild.id, member.id)

        # Optionally add Unverified role back
        unverified_name = os.getenv("AUTH_UNVERIFIED_ROLE", "Unverified")
        unver_role = discord.utils.get(guild.roles, name=unverified_name)
        if unver_role:
            try:
                await member.add_roles(unver_role, reason="Verification revoked")
            except Exception:
                pass
        
        msg = t("revoke_success", get_lang(guild.id, interaction.user.id), member=member.mention)
        if removed_role:
            msg += t("revoke_role_removed", get_lang(guild.id, interaction.user.id))
        if removed_db:
            msg += t("revoke_record_cleared", get_lang(guild.id, interaction.user.id))

        await interaction.followup.send(msg, ephemeral=True)

    @revoke.error
    async def revoke_error(self, interaction: Interaction, error: Exception):
        try:
            from discord.app_commands.errors import MissingPermissions
        except Exception:
            MissingPermissions = tuple()  # type: ignore
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(t("missing_admin", get_lang(interaction.guild.id if interaction.guild else 0, interaction.user.id)), ephemeral=True)
        else:
            if interaction.response.is_done():
                await interaction.followup.send(t("generic_error", get_lang(interaction.guild.id if interaction.guild else 0, interaction.user.id)), ephemeral=True)
            else:
                await interaction.response.send_message(t("generic_error", get_lang(interaction.guild.id if interaction.guild else 0, interaction.user.id)), ephemeral=True)

