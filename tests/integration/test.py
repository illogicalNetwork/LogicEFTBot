import unittest
import subprocess


class TwitchIntegrationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        1. Generate a settings.json file.
        2. Start the twitch bot process
        3. Wait for it to connect.
        4. Start the fakeClient, wait for it to connect.
        """
        pass

    @classmethod
    def tearDownClass(cls):
        """
        1. Kill the fakeClient.
        2. Kill the bot.
        """
        pass



    def test
