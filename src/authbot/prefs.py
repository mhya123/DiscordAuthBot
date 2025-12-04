from __future__ import annotations

from .storage import get_db


def set_lang(guild_id: int, user_id: int, lang: str) -> None:
    """设置用户的语言偏好"""
    get_db().set_lang(guild_id, user_id, lang)


def get_lang(guild_id: int, user_id: int) -> str:
    """获取用户的语言偏好，默认为 zh"""
    try:
        return get_db().get_lang(guild_id, user_id)
    except Exception:
        return "zh"
