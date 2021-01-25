
import mysql.connector as mysql
from .config import settings
from typing import List

class Database:
    def __init__(self) -> None:
        db = mysql.connect(
            host = settings["database_config"]["host"],
            user = settings["database_config"]["user"],
            passwd = settings["database_config"]["passwd"],
            database = settings["database_config"]["database"]
        )

        sql = db.cursor(buffered=True)
        db.commit()
        self.db = db
        self.sql = sql

    def update_cooldown(self, name: str, cooldown: int) -> None:
        self.sql.execute("REPLACE INTO channels (name, cooldown) VALUES (%s, %s)", (name, cooldown))
        self.db.commit()

    def update_lang(self, name: str, lang: str, uname: str) -> None:
        #self.sql.execute("UPDATE users SELECT username, lang VALUES (%s, %s)", (name, lang))
        self.sql.execute("UPDATE users SET username=%s, lang=%s WHERE username=%s", (name,lang, uname))
        self.db.commit()

    def get_cd(self, name: str) -> int:
        self.sql.execute("SELECT cooldown FROM channels WHERE name = %s", (name,))
        cd = self.sql.fetchone()
        return cd[0] if cd else None

    def get_lang(self, name: str) -> str:
        self.sql.execute("SELECT lang FROM users WHERE username = %s", (name,))
        lang = self.sql.fetchone()
        return lang[0] if lang else settings["default_lang"]

    def get_channels(self) -> List[str]:
        self.db.commit()
        self.sql.execute("SELECT username from users")
        return [i[0] for i in self.sql.fetchall()]

#exported global variables/objects
db = Database()
