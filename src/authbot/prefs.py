from __future__ import annotations

from . import storage


def set_lang(guild_id: int, user_id: int, lang: str) -> None:
    db = storage.load_db()
    guilds = db.setdefault("guilds", {})
    g = guilds.setdefault(str(guild_id), {})
    langs = g.setdefault("lang", {})
    langs[str(user_id)] = lang
    storage.save_db(db)


def get_lang(guild_id: int, user_id: int) -> str:
    db = storage.load_db()
    try:
        return db.get("guilds", {}).get(str(guild_id), {}).get("lang", {}).get(str(user_id), "zh")
    except Exception:
        return "zh"
