from __future__ import annotations

import json
import os
import tempfile
from typing import Dict, Any

DEFAULT_PATH = os.getenv("AUTH_DATA_FILE", os.path.abspath(os.path.join(os.getcwd(), "data.json")))


def _ensure_parent(path: str) -> None:
    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)


def load_db(path: str = DEFAULT_PATH) -> Dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"guilds": {}}
    except Exception:
        return {"guilds": {}}


def save_db(db: Dict[str, Any], path: str = DEFAULT_PATH) -> None:
    _ensure_parent(path)
    tmp_fd, tmp_path = tempfile.mkstemp(prefix="data.json.", suffix=".tmp", dir=os.path.dirname(path) or None)
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, path)
    finally:
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass


def ensure_db_exists(path: str = DEFAULT_PATH) -> None:
    if not os.path.exists(path):
        save_db({"guilds": {}}, path)


def is_verified(guild_id: int, user_id: int, path: str = DEFAULT_PATH) -> bool:
    db = load_db(path)
    return str(user_id) in db.get("guilds", {}).get(str(guild_id), {}).get("verified", {})


def mark_verified(guild_id: int, user_id: int, record: Dict[str, Any], path: str = DEFAULT_PATH) -> None:
    db = load_db(path)
    guilds = db.setdefault("guilds", {})
    g = guilds.setdefault(str(guild_id), {})
    verified = g.setdefault("verified", {})
    verified[str(user_id)] = record
    save_db(db, path)


def revoke_verified(guild_id: int, user_id: int, path: str = DEFAULT_PATH) -> bool:
    db = load_db(path)
    g = db.get("guilds", {}).get(str(guild_id))
    if not g:
        return False
    verified = g.get("verified", {})
    existed = str(user_id) in verified
    if existed:
        verified.pop(str(user_id), None)
        save_db(db, path)
        return True
    return False
