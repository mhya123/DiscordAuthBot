from __future__ import annotations

import os
import logging
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from contextlib import contextmanager

log = logging.getLogger("authbot.storage")

DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()
DB_PATH = os.getenv("DB_PATH", os.path.abspath(os.path.join(os.getcwd(), "data.db")))
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "authbot")


class DatabaseBackend(ABC):
    @abstractmethod
    def init_tables(self) -> None:
        pass
    
    @abstractmethod
    def is_verified(self, guild_id: int, user_id: int) -> bool:
        pass
    
    @abstractmethod
    def mark_verified(self, guild_id: int, user_id: int, username: str) -> None:
        pass
    
    @abstractmethod
    def revoke_verified(self, guild_id: int, user_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_user_info(self, guild_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def get_verified_users(self, guild_id: int) -> Dict[str, Dict[str, Any]]:
        pass
    
    @abstractmethod
    def set_lang(self, guild_id: int, user_id: int, lang: str) -> None:
        pass
    
    @abstractmethod
    def get_lang(self, guild_id: int, user_id: int) -> str:
        pass


class SQLiteBackend(DatabaseBackend):
    def __init__(self, db_path: str = DB_PATH):
        import sqlite3
        self.db_path = db_path
        self._ensure_parent()
        self.init_tables()
    
    def _ensure_parent(self) -> None:
        parent = os.path.dirname(self.db_path)
        if parent and not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)
    
    @contextmanager
    def _get_conn(self):
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()
    
    def init_tables(self) -> None:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS verified_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    username TEXT NOT NULL,
                    verified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(guild_id, user_id)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_prefs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    lang TEXT DEFAULT 'zh',
                    UNIQUE(guild_id, user_id)
                )
            ''')
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_verified_guild ON verified_users(guild_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_verified_user ON verified_users(guild_id, user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_prefs_user ON user_prefs(guild_id, user_id)")
        log.info("SQLite database initialized: %s", self.db_path)
    
    def is_verified(self, guild_id: int, user_id: int) -> bool:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM verified_users WHERE guild_id = ? AND user_id = ?",
                (str(guild_id), str(user_id))
            )
            return cursor.fetchone() is not None
    
    def mark_verified(self, guild_id: int, user_id: int, username: str) -> None:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO verified_users (guild_id, user_id, username)
                VALUES (?, ?, ?)
                ON CONFLICT(guild_id, user_id) DO UPDATE SET 
                    username = excluded.username,
                    verified_at = CURRENT_TIMESTAMP
            ''', (str(guild_id), str(user_id), username))
    
    def revoke_verified(self, guild_id: int, user_id: int) -> bool:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM verified_users WHERE guild_id = ? AND user_id = ?",
                (str(guild_id), str(user_id))
            )
            return cursor.rowcount > 0
    
    def get_user_info(self, guild_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT username, verified_at FROM verified_users WHERE guild_id = ? AND user_id = ?",
                (str(guild_id), str(user_id))
            )
            row = cursor.fetchone()
            if row:
                return {"username": row["username"], "verified_at": row["verified_at"]}
            return None
    
    def get_verified_users(self, guild_id: int) -> Dict[str, Dict[str, Any]]:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_id, username, verified_at FROM verified_users WHERE guild_id = ?",
                (str(guild_id),)
            )
            result = {}
            for row in cursor.fetchall():
                result[row["user_id"]] = {
                    "username": row["username"],
                    "verified_at": row["verified_at"]
                }
            return result
    
    def set_lang(self, guild_id: int, user_id: int, lang: str) -> None:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO user_prefs (guild_id, user_id, lang)
                VALUES (?, ?, ?)
                ON CONFLICT(guild_id, user_id) DO UPDATE SET lang = excluded.lang
            ''', (str(guild_id), str(user_id), lang))
    
    def get_lang(self, guild_id: int, user_id: int) -> str:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT lang FROM user_prefs WHERE guild_id = ? AND user_id = ?",
                (str(guild_id), str(user_id))
            )
            row = cursor.fetchone()
            return row["lang"] if row else "zh"


class MySQLBackend(DatabaseBackend):
    def __init__(self, host: str = DB_HOST, port: int = DB_PORT, 
                 user: str = DB_USER, password: str = DB_PASSWORD, 
                 database: str = DB_NAME):
        self.config = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database,
        }
        self.init_tables()
    
    @contextmanager
    def _get_conn(self):
        import pymysql
        conn = pymysql.connect(
            **self.config,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()
    
    def init_tables(self) -> None:
        import pymysql
        config_no_db = {k: v for k, v in self.config.items() if k != "database"}
        conn = pymysql.connect(**config_no_db, charset='utf8mb4')
        try:
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{self.config['database']}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            conn.commit()
        finally:
            conn.close()
        
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS verified_users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    guild_id VARCHAR(32) NOT NULL,
                    user_id VARCHAR(32) NOT NULL,
                    username VARCHAR(128) NOT NULL,
                    verified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    UNIQUE KEY unique_guild_user (guild_id, user_id),
                    INDEX idx_guild (guild_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_prefs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    guild_id VARCHAR(32) NOT NULL,
                    user_id VARCHAR(32) NOT NULL,
                    lang VARCHAR(8) DEFAULT 'zh',
                    UNIQUE KEY unique_guild_user (guild_id, user_id),
                    INDEX idx_guild_user (guild_id, user_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            ''')
        log.info("MySQL database initialized: %s@%s:%d/%s", 
                 self.config['user'], self.config['host'], 
                 self.config['port'], self.config['database'])
    
    def is_verified(self, guild_id: int, user_id: int) -> bool:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM verified_users WHERE guild_id = %s AND user_id = %s",
                (str(guild_id), str(user_id))
            )
            return cursor.fetchone() is not None
    
    def mark_verified(self, guild_id: int, user_id: int, username: str) -> None:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO verified_users (guild_id, user_id, username)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    username = VALUES(username),
                    verified_at = CURRENT_TIMESTAMP
            ''', (str(guild_id), str(user_id), username))
    
    def revoke_verified(self, guild_id: int, user_id: int) -> bool:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM verified_users WHERE guild_id = %s AND user_id = %s",
                (str(guild_id), str(user_id))
            )
            return cursor.rowcount > 0
    
    def get_user_info(self, guild_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT username, verified_at FROM verified_users WHERE guild_id = %s AND user_id = %s",
                (str(guild_id), str(user_id))
            )
            row = cursor.fetchone()
            if row:
                return {"username": row["username"], "verified_at": str(row["verified_at"])}
            return None
    
    def get_verified_users(self, guild_id: int) -> Dict[str, Dict[str, Any]]:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_id, username, verified_at FROM verified_users WHERE guild_id = %s",
                (str(guild_id),)
            )
            result = {}
            for row in cursor.fetchall():
                result[row["user_id"]] = {
                    "username": row["username"],
                    "verified_at": str(row["verified_at"])
                }
            return result
    
    def set_lang(self, guild_id: int, user_id: int, lang: str) -> None:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO user_prefs (guild_id, user_id, lang)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE lang = VALUES(lang)
            ''', (str(guild_id), str(user_id), lang))
    
    def get_lang(self, guild_id: int, user_id: int) -> str:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT lang FROM user_prefs WHERE guild_id = %s AND user_id = %s",
                (str(guild_id), str(user_id))
            )
            row = cursor.fetchone()
            return row["lang"] if row else "zh"


# ==================== 全局实例 ====================

_db: Optional[DatabaseBackend] = None


def get_db() -> DatabaseBackend:
    global _db
    if _db is None:
        if DB_TYPE == "mysql":
            log.info("Using MySQL database backend")
            _db = MySQLBackend()
        else:
            log.info("Using SQLite database backend")
            _db = SQLiteBackend()
    return _db


def ensure_db_exists() -> None:
    get_db()


# ==================== 兼容性 API ====================

def is_verified(guild_id: int, user_id: int) -> bool:
    return get_db().is_verified(guild_id, user_id)


def mark_verified(guild_id: int, user_id: int, record: Dict[str, Any]) -> None:
    username = record.get("username", "user")
    get_db().mark_verified(guild_id, user_id, username)


def revoke_verified(guild_id: int, user_id: int) -> bool:
    return get_db().revoke_verified(guild_id, user_id)


def get_user_info(guild_id: int, user_id: int) -> Optional[Dict[str, Any]]:
    return get_db().get_user_info(guild_id, user_id)


def get_verified_users(guild_id: int) -> Dict[str, Dict[str, Any]]:
    return get_db().get_verified_users(guild_id)


def load_db() -> Dict[str, Any]:
    log.warning("load_db() is deprecated, use get_db() methods instead")
    return {"guilds": {}}


def save_db(db: Dict[str, Any]) -> None:
    log.warning("save_db() is deprecated, use get_db() methods instead")
    pass