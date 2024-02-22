from typing import List, Optional, Dict


class MockDatabase:
    """
    An in-memory not-so-correct implementation of the mysql db.
    """

    _cooldowns = {"#lvndmark": 10, "#logicalsolutions": 15}
    _lang = {"#lvndmark": "en", "#logicalsolutions": "ru"}

    @staticmethod
    def get():
        return MockDatabase()

    def update_cooldown(self, name: str, cooldown: int) -> None:
        MockDatabase._cooldowns[name] = cooldown

    def update_lang(self, name: str, lang: str, uname: str) -> None:
        MockDatabase._lang[name] = lang

    def get_cd(self, name: str) -> int:
        return MockDatabase._cooldowns[name]

    def get_lang(self, name: str) -> str:
        return MockDatabase._lang[name]

    def get_channels(self) -> List[str]:
        return ["#lvndmark", "#logicalsolutions"]

    def sql_log(self, sourcetype: str, source: str, cmd: str, query: Optional[str]):
        pass

    def get_command_aliases(self, channel: str) -> Optional[Dict[str, str]]:
        return None
