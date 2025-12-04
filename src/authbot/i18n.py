from __future__ import annotations

from typing import Dict, Any

DEFAULT_LANG = "zh"

_messages: Dict[str, Dict[str, str]] = {
    # ==================== 通用消息 ====================
    "must_use_in_server": {
        "zh": "此命令必须在服务器内使用。",
        "en": "This command must be used in a server.",
    },
    "use_channel": {
        "zh": "请在 #{channel} 中使用该命令。",
        "en": "Please use this command in #{channel}.",
    },
    "generic_error": {
        "zh": "运行此命令时发生错误。",
        "en": "An error occurred while running this command.",
    },

    # ==================== 认证相关 ====================
    "api_not_config": {
        "zh": "认证 API 未配置。",
        "en": "Auth API base is not configured.",
    },
    "already_verified": {
        "zh": "你已通过验证，无需重复认证。",
        "en": "You are already verified.",
    },
    "auth_failed_500": {
        "zh": "账号或密码错误，请检查后重试。",
        "en": "Incorrect username or password. Please check and try again.",
    },
    "auth_failed_generic": {
        "zh": "认证失败，请稍后再试。",
        "en": "Authentication failed. Please try again later.",
    },
    "auth_success": {
        "zh": "✅ 已以 **{username}** 身份通过验证！已授予角色并更新昵称。",
        "en": "✅ Authenticated as **{username}**! Role granted and nickname updated.",
    },
    "auth_request_failed": {
        "zh": "认证请求失败：{error}",
        "en": "Auth request failed: {error}",
    },
    "auth_partial_success": {
        "zh": "已验证为 **{username}**，但是：{error}",
        "en": "Authenticated as **{username}**, but: {error}",
    },

    # ==================== 登录模态框 ====================
    "modal_title": {
        "zh": "🔐 账号登录",
        "en": "🔐 Account Login",
    },
    "modal_login_label": {
        "zh": "登录名（用户名/邮箱）",
        "en": "Login (username/email)",
    },
    "modal_login_placeholder": {
        "zh": "请输入你的用户名或邮箱",
        "en": "Enter your username or email",
    },
    "modal_password_label": {
        "zh": "密码",
        "en": "Password",
    },

    # ==================== Setup 相关 ====================
    "setup_complete": {
        "zh": "✅ 初始化完成！\n• 角色：{role}\n• 频道：{channel}\n\n已在验证频道发送欢迎消息。",
        "en": "✅ Setup complete!\n• Role: {role}\n• Channel: {channel}\n\nWelcome message sent to auth channel.",
    },
    "welcome_message": {
        "zh": "欢迎来到本服务器！请完成身份验证以获得完整访问权限。\n\nWelcome! Please verify your identity to get full access.",
        "en": "Welcome to this server! Please verify your identity to get full access.\n\n欢迎！请完成身份验证以获得完整访问权限。",
    },
    "welcome_instructions": {
        "zh": "1️⃣ 选择你的显示语言\n2️⃣ 点击「登录验证」按钮\n3️⃣ 输入你的账号和密码\n4️⃣ 验证成功后即可访问其他频道",
        "en": "1️⃣ Choose your display language\n2️⃣ Click the 'Login' button\n3️⃣ Enter your credentials\n4️⃣ After verification, you can access other channels",
    },

    # ==================== 语言相关 ====================
    "lang_prompt": {
        "zh": "请选择显示语言 / Choose your language",
        "en": "Choose your language / 请选择显示语言",
    },
    "lang_set_zh": {
        "zh": "✅ 已切换为中文显示。",
        "en": "✅ Switched to Chinese.",
    },
    "lang_set_en": {
        "zh": "✅ 已切换为英文显示。",
        "en": "✅ Switched to English.",
    },

    # ==================== 权限相关 ====================
    "missing_admin": {
        "zh": "⚠️ 需要管理员权限才能使用此命令。",
        "en": "⚠️ You need Administrator permission to use this command.",
    },
    "guild_not_found": {
        "zh": "找不到服务器。",
        "en": "Guild not found.",
    },
    "role_create_failed": {
        "zh": "无法创建/找到角色。",
        "en": "Failed to create/find role.",
    },
    "role_permission_denied": {
        "zh": "缺少分配角色的权限。请将机器人的角色提升到更高位置。",
        "en": "Missing permission to assign roles. Move the bot's role higher.",
    },
    "role_assign_failed": {
        "zh": "分配角色失败：{error}",
        "en": "Failed to assign role: {error}",
    },

    # ==================== 撤销相关 ====================
    "revoke_success": {
        "zh": "✅ 已撤销 {member} 的验证。",
        "en": "✅ Revoked verification for {member}.",
    },
    "revoke_role_removed": {
        "zh": " 已移除角色。",
        "en": " Removed role.",
    },
    "revoke_record_cleared": {
        "zh": " 已清除记录。",
        "en": " Cleared record.",
    },

    # ==================== 状态查询 ====================
    "status_verified_title": {
        "zh": "已验证",
        "en": "Verified",
    },
    "status_verified_desc": {
        "zh": "你已通过身份验证，账号名：**{username}**",
        "en": "You are verified as **{username}**",
    },
    "status_role": {
        "zh": "当前角色",
        "en": "Current Role",
    },
    "status_unverified_title": {
        "zh": "未验证",
        "en": "Not Verified",
    },
    "status_unverified_desc": {
        "zh": "你还没有完成身份验证。",
        "en": "You have not completed verification yet.",
    },
    "status_how_to": {
        "zh": "如何验证？",
        "en": "How to verify?",
    },
    "status_how_to_desc": {
        "zh": "使用 `/login` 命令或点击验证频道中的按钮开始验证。",
        "en": "Use `/login` command or click the button in auth channel to start.",
    },

    # ==================== 用户列表 ====================
    "no_verified_users": {
        "zh": "暂无已验证用户。",
        "en": "No verified users yet.",
    },
    "verified_list_title": {
        "zh": "📋 已验证用户列表",
        "en": "📋 Verified Users List",
    },

    # ==================== 帮助系统 ====================
    "help_title": {
        "zh": "使用帮助",
        "en": "Help",
    },
    "help_description": {
        "zh": "这是一个身份验证机器人，用于验证用户身份并授予相应权限。",
        "en": "This is an authentication bot for verifying user identity and granting access.",
    },
    "help_user_commands": {
        "zh": "用户命令",
        "en": "User Commands",
    },
    "help_admin_commands": {
        "zh": "管理员命令",
        "en": "Admin Commands",
    },
    "help_login_desc": {
        "zh": "登录验证账号",
        "en": "Login to verify account",
    },
    "help_status_desc": {
        "zh": "查看你的验证状态",
        "en": "Check your verification status",
    },
    "help_lang_desc": {
        "zh": "切换显示语言",
        "en": "Switch display language",
    },
    "help_help_desc": {
        "zh": "显示此帮助信息",
        "en": "Show this help message",
    },
    "help_setup_desc": {
        "zh": "初始化认证系统",
        "en": "Initialize auth system",
    },
    "help_revoke_desc": {
        "zh": "撤销用户的验证",
        "en": "Revoke user verification",
    },
    "help_list_desc": {
        "zh": "查看已验证用户列表",
        "en": "List verified users",
    },
    "help_panel_desc": {
        "zh": "发送验证面板卡片",
        "en": "Send auth panel card",
    },

    # ==================== 验证面板 ====================
    "panel_sent": {
        "zh": "✅ 验证面板已发送到 {channel}",
        "en": "✅ Auth panel sent to {channel}",
    },
    "panel_no_permission": {
        "zh": "❌ 没有权限在该频道发送消息。",
        "en": "❌ No permission to send messages in that channel.",
    },
    "invalid_channel": {
        "zh": "❌ 无效的频道。",
        "en": "❌ Invalid channel.",
    },
}


def t(key: str, lang: str, **kwargs: Any) -> str:
    """获取翻译文本"""
    lang = (lang or DEFAULT_LANG).split("-")[0]
    bundle = _messages.get(key, {})
    template = bundle.get(lang) or bundle.get("en") or bundle.get("zh") or key
    try:
        return template.format(**kwargs)
    except Exception:
        return template
