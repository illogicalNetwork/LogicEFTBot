import unittest
from tests.integration.test import TwitchIntegrationTest

class LogicEFTBotIntegrationTest(TwitchIntegrationTest):

    def test_price_works(self):
        """
        Test that if, someone in chat types "!price slick"
        The bot will respond with the following python-compatible
        regex.
        """
        self.chatmember_say("!price slick")
        self.expect_reply(r"The price of (.+?) is (.*?)", timeout=30)
