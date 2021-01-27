import unittest
import logging
from unittest import mock
from typing import List
from bot.log import log
from bot.bot import LogicEFTBot
from bot.config import settings, localized_string
from bot.base import CommandContext, AuthorInfo
from bot.database import Database
from tests.network import mocked_requests_get, mock_url_get, mock_url_reset
from tests.dbutil import MockDatabase
import requests

@mock.patch('bot.bot.requests.get', side_effect=mocked_requests_get)
@mock.patch('bot.eft.requests.get', side_effect=mocked_requests_get)
@mock.patch('bot.bot.Database', MockDatabase)
class TestLogicEFTBot(unittest.TestCase):
    """
    A suite of tests verifying that the commands
    in the logic eft bot behave correctly.
    """
    def setUp(self):
        log.setLevel(logging.WARNING) # ignore info.
        self.bot = LogicEFTBot()
        self.fake_context = CommandContext(author=AuthorInfo(name="me", is_mod=False), channel="#lvndmark")

    def tearDown(self):
        mock_url_reset()

    def test_price(self, mock_one, mock_two):
        mock_url_get("http://price.fakeapi.com", "fake_response")
        settings["price_link"]["en"] = "http://price.fakeapi.com"
        settings["price_link"]["ru"] = "http://price.fakeapi.com"
        response = self.bot.exec(self.fake_context, "price", "anything")
        self.assertEqual(response, "@me fake_response")

    def test_slot(self, mock_one, mock_two):
        mock_url_get("http://slot.fakeapi.com", "fake_response_slot")
        settings["slot_link"]["en"] = "http://slot.fakeapi.com"
        settings["slot_link"]["ru"] = "http://slot.fakeapi.com"
        response = self.bot.exec(self.fake_context, "slot", "anything")
        self.assertEqual(response, "@me fake_response_slot")

    def test_wiki(self, mock_one, mock_two):
        mock_url_get("http://wiki.fakeapi.com", "fake_wiki")
        settings["wiki_link"]["en"] = "http://wiki.fakeapi.com"
        settings["wiki_link"]["ru"] = "http://wiki.fakeapi.com"
        response = self.bot.exec(self.fake_context, "wiki", "anything")
        self.assertEqual(response, "@me fake_wiki")

    def test_astat(self, mock_one, mock_two):
        mock_url_get("http://astat.fakeapi.com", "fake_astat")
        settings["ammo_link"]["en"] = "http://astat.fakeapi.com"
        settings["ammo_link"]["ru"] = "http://astat.fakeapi.com"
        response = self.bot.exec(self.fake_context, "astat", "anything")
        self.assertEqual(response, "@me fake_astat")

    def test_medical(self, mock_one, mock_two):
        mock_url_get("http://medical.fakeapi.com", "fake_medical")
        settings["medical_link"]["en"] = "http://medical.fakeapi.com"
        settings["medical_link"]["ru"] = "http://medical.fakeapi.com"
        response = self.bot.exec(self.fake_context, "medical", "anything")
        self.assertEqual(response, "@me fake_medical")

    def test_armor(self, mock_one, mock_two):
        mock_url_get("http://armor.fakeapi.com", "fake_armor")
        settings["armor_link"]["en"] = "http://armor.fakeapi.com"
        settings["armor_link"]["ru"] = "http://armor.fakeapi.com"
        response = self.bot.exec(self.fake_context, "armor", "anything")
        self.assertEqual(response, "@me fake_armor")

    def test_eft_bot(self, mock_one, mock_two):
        response = self.bot.exec(self.fake_context, "eftbot", "fake_bot")
        self.assertEqual(response, "@me - {}".format(localized_string("en", "botHelp")))

    def test_bot_help(self, mock_one, mock_two):
        response = self.bot.exec(self.fake_context, "help", "fake_help")
        self.assertEqual(response, "@me - {}".format(localized_string("en", "botHelp")))

    def test_add_bot(self, mock_one, mock_two):
        response = self.bot.exec(self.fake_context, "addbot", "fake_add_bot")
        self.assertEqual(response, "@me - {}".format(localized_string("en", "addBot")))

    def test_cd(self, mock_one, mock_two):
        pass

    def test_set_lang(self, mock_one, mock_two):
        pass

if __name__ == '__main__':
    unittest.main()
