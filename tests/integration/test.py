import unittest
import subprocess
import threading
from tests.integration.chatmember import ChatMember, ChatMemberCommand, ChatMemberResponse
from queue import SimpleQueue, Empty
from typing import Callable
import dataclasses
import json
import time

CHAT_MEMBER_QUEUE : SimpleQueue = SimpleQueue()
CHAT_MEMBER_COMMANDS : SimpleQueue = SimpleQueue()
TEST_CHANNEL = "pawn_star"

def run_chat_member():
    global CHAT_MEMBER_COMMANDS
    global CHAT_MEMBER_QUEUE
    global IRC_SPEC
    chat_member = ChatMember(outbound=CHAT_MEMBER_QUEUE, inbound=CHAT_MEMBER_COMMANDS, channel=TEST_CHANNEL)
    chat_member.start() # this runs forever.


class TwitchIntegrationTest(unittest.TestCase):

    @classmethod
    def expect_chatmember_response(cls, fn: Callable[[ChatMemberResponse], bool], timeout : int = 5, error_message: str = ''):
        """
        Expect that the ChatMember will provide a response which satisfies some function, within
        the timeframe given.
        """
        time_end = time.time() + timeout
        while time.time() < time_end:
            # poll for responses.
            max_wait = max(time_end - time.time(), 2)
            try:
                message = CHAT_MEMBER_QUEUE.get(True, timeout=max_wait)
                if message:
                    print(json.dumps(dataclasses.asdict(message)))
                if message and fn(message):
                    return
            except Empty:
                # keep going
                continue
        raise Exception(f'No suitable response was found within the timeout given. {error_message}')

    def setUp(self):
        self.assertTrue(self.is_chatmember_running, f"Failed to start up ChatMember: {self.error_msg}")


    @classmethod
    def setUpClass(cls):
        """
        1. Start the fakeClient, wait for it to connect.
        2. Start the twitch bot thread
        3. Wait for it to connect.
        """
        # start thread
        cls.chat_member_thread = threading.Thread(target=run_chat_member, args=())
        cls.chat_member_thread.start()
        cls.is_chatmember_running = True
        # expect a welcome within 10 seconds.
        try:
            cls.expect_chatmember_response(lambda message: message.connected, timeout=30, error_message="Failed to connect to twitch.")
            cls.expect_chatmember_response(lambda message: message.welcome, timeout=30, error_message="Failed to get welcome from twitch.")
        except Exception as e:
            cls.is_chatmember_running = False
            cls.error_msg = str(e)

    @classmethod
    def tearDownClass(cls):
        """
        1. Kill the fakeClient.
        2. Kill the bot.
        """
        global CHAT_MEMBER_COMMANDS
        print("Shutting down ChatMember service.")
        CHAT_MEMBER_COMMANDS.put(ChatMemberCommand(exit=True))
        cls.expect_chatmember_response(lambda message: message.shutdown, timeout=10, error_message="Failed to shutdown bot in time.")
        cls.chat_member_thread.join()
