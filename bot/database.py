from __future__ import annotations  # type: ignore
import mysql.connector as mysql
from mysql.connector import pooling
from bot.config import settings
from bot.log import log
from typing import List, Optional
import datetime


class Database:
    singleton = None

    @staticmethod
    def get(recreate=False) -> Database:
        if recreate or not Database.singleton:
            # exported global variables/objects
            Database.singleton = Database()
        return Database.singleton

    def __init__(self) -> None:
        log.info("Connecting to MySQL...")
        db = mysql.connect(
            host=settings["database_config"]["host"],
            user=settings["database_config"]["user"],
            passwd=settings["database_config"]["passwd"],
            database=settings["database_config"]["database"],
        )
        log.info("Connected.")
        sql = db.cursor(buffered=True)
        db.commit()
        self.db = db
        self.sql = sql

    def update_cooldown(self, name: str, cooldown: int) -> None:
        self.sql.execute(
            "UPDATE users SET cooldown=%s WHERE username=%s", (int(cooldown), name)
        )
        self.db.commit()

    def update_lang(self, name: str, lang: str, uname: str) -> None:
        # self.sql.execute("UPDATE users SELECT username, lang VALUES (%s, %s)", (name, lang))
        self.sql.execute("UPDATE users SET lang=%s WHERE username=%s", (lang, uname))
        self.db.commit()

    def get_cd(self, name: str) -> int:
        self.sql.execute("SELECT cooldown FROM users WHERE username=%s", (name,))
        cd = self.sql.fetchone()
        return int(cd[0]) if cd else int(settings["default_cooldown"])

    def get_lang(self, name: str) -> str:
        self.sql.execute("SELECT lang FROM users WHERE username = %s", (name,))
        lang = self.sql.fetchone()
        return str(lang[0]) if lang else str(settings["default_lang"])

    def get_channels(self) -> List[str]:
        self.db.commit()
        self.sql.execute("SELECT username from users")
        return [i[0] for i in self.sql.fetchall()]

    def sql_log(
        self, sourcetype: str, source: str, cmd: str, query: Optional[str]
    ) -> None:
        ts = datetime.datetime.utcnow()
        self.sql.execute(
            "INSERT INTO bot_logging (timestamp, source, channel, search_type, query) VALUES (%s, %s, %s, %s, %s)",
            (ts, sourcetype, source, cmd, query),
        )
        self.db.commit()


def check_lang(channel_name: str) -> str:
    return Database.get().get_lang(channel_name)
