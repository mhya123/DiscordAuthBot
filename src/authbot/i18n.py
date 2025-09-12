from __future__ import annotations

from typing import Dict, Any

DEFAULT_LANG = "zh"

_messages: Dict[str, Dict[str, str]] = {
    "must_use_in_server": {
        "zh": "此命令必须在服务器内使用。",
        "en": "This command must be used in a server.",
    },
    "use_channel": {
        "zh": "请在 #{channel} 中使用该命令。",
        "en": "Please use this command in #{channel}.",
    },
    "api_not_config": {
        "zh": "认证 API 未配置。",
        "en": "Auth API base is not configured.",
    },
    "already_verified": {
        "zh": "你已通过验证，无需重复认证。",
        "en": "You are already verified.",
    },
    "auth_failed_500": {
        "zh": "账号或密码错误。",
        "en": "Incorrect username or password.",
    },
    "auth_failed_generic": {
        "zh": "认证失败，请稍后再试。",
        "en": "Authentication failed. Please try again later.",
    },
    "auth_success": {
        "zh": "✅ 已以 {username} 身份通过验证，已授予角色并更新昵称。",
        "en": "✅ Authenticated as {username}. Role granted and nickname updated.",
    },
    "setup_complete": {
        "zh": "初始化完成。角色：{role}，频道：{channel}",
        "en": "Setup complete. Role: {role}, Channel: {channel}",
    },
    "lang_prompt": {
        "zh": "请选择显示语言 / Choose your language",
        "en": "请选择显示语言 / Choose your language",
    },
    "lang_set_zh": {
        "zh": "已切换为中文显示。",
        "en": "Switched to Chinese.",
    },
    "lang_set_en": {
        "zh": "已切换为英文显示。",
        "en": "Switched to English.",
    },
    "missing_admin": {
        "zh": "需要管理员权限才能使用此命令。",
        "en": "You need Administrator permission to use this command.",
    },
    "guild_not_found": {
        "zh": "找不到服务器。",
        "en": "Guild not found",
    },
    "role_create_failed": {
        "zh": "无法创建/找到角色。",
        "en": "Failed to create/find role",
    },
    "role_permission_denied": {
        "zh": "缺少分配角色的权限。请将我的角色提升到更高位置。",
        "en": "Missing permission to assign roles. Move my role higher.",
    },
    "role_assign_failed": {
        "zh": "分配角色失败：{error}",
        "en": "Failed to assign role: {error}",
    },
    "modal_title": {
        "zh": "账号登录",
        "en": "Account Login",
    },
    "modal_login_label": {
        "zh": "登录名（用户名/邮箱）",
        "en": "Login (username/email)",
    },
    "modal_login_placeholder": {
        "zh": "你的用户名或邮箱",
        "en": "your name or email",
    },
    "modal_password_label": {
        "zh": "密码",
        "en": "Password",
    },
    "auth_request_failed": {
        "zh": "认证请求失败：{error}",
        "en": "Auth request failed: {error}",
    },
    "auth_partial_success": {
        "zh": "已验证为 {username}，但是：{error}",
        "en": "Authenticated as {username}, but: {error}",
    },
    "revoke_success": {
        "zh": "已撤销 {member} 的验证。",
        "en": "Revoked verification for {member}.",
    },
    "revoke_role_removed": {
        "zh": " 已移除角色。",
        "en": " Removed role.",
    },
    "revoke_record_cleared": {
        "zh": " 已清除记录。",
        "en": " Cleared record.",
    },
    "generic_error": {
        "zh": "运行此命令时发生错误。",
        "en": "An error occurred while running this command.",
    },
}


def t(key: str, lang: str, **kwargs: Any) -> str:
    lang = (lang or DEFAULT_LANG).split("-")[0]
    bundle = _messages.get(key, {})
    template = bundle.get(lang) or bundle.get("en") or bundle.get("zh") or key
    try:
        return template.format(**kwargs)
    except Exception:
        return template
