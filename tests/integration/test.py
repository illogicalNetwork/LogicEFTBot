import unittest
import subprocess
import threading
from twitch_master import main, abort_bot
from tests.integration.chatmember import ChatMember, ChatMemberCommand, ChatMemberResponse, NICK
from queue import SimpleQueue, Empty
from typing import Callable
import dataclasses
import json
import time
import re
import subprocess

CHAT_MEMBER_QUEUE : SimpleQueue = SimpleQueue()
CHAT_MEMBER_COMMANDS : SimpleQueue = SimpleQueue()
TEST_CHANNEL = "pawn_star"

def run_chat_member():
    global CHAT_MEMBER_COMMANDS
    global CHAT_MEMBER_QUEUE
    global IRC_SPEC
    chat_member = ChatMember(outbound=CHAT_MEMBER_QUEUE, inbound=CHAT_MEMBER_COMMANDS)
    chat_member.start() # this runs forever.


class TwitchIntegrationTest(unittest.TestCase):

    # Set to true to enable printing events.
    VERBOSE = True

    @classmethod
    def expect_reply(cls, matching: str, timeout: int = 5, error_message: str = '') -> None:
        def is_valid_response(response: ChatMemberResponse) -> bool:
            if response.message:
                return re.search(matching, response.message)
            return False
        cls.expect_chatmember_response(is_valid_response, timeout, error_message)

    @classmethod
    def expect_chatmember_response(cls, fn: Callable[[ChatMemberResponse], bool], timeout : int = 5, error_message: str = '') -> None:
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
                if message and cls.VERBOSE:
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
    def chatmember_say(cls, text: str):
        CHAT_MEMBER_COMMANDS.put(ChatMemberCommand(say=text))

    @classmethod
    def setUpClass(cls):
        """
        1. Start ChatMember, wait for it to connect.
        2. Wait for it to connect.
        3. Start Bot.
        4. Wait for it to connect.
        """
        # start thread
        cls.chat_member_thread = threading.Thread(target=run_chat_member, args=())
        cls.chat_member_thread.start()
        cls.is_chatmember_running = True
        cls.error_msg = None

        cls.bot_thread = threading.Thread(target=main, args=())
        cls.bot_thread.start()
        # expect a welcome within 10 seconds.
        try:
            cls.expect_chatmember_response(lambda message: message.connected, timeout=30, error_message="Failed to connect to twitch.")
            cls.expect_chatmember_response(lambda message: message.welcome, timeout=30, error_message="Failed to get welcome from twitch.")
            time.sleep(5)
            CHAT_MEMBER_COMMANDS.put(ChatMemberCommand(join=NICK))
            # Wait for the bot to connect.
            print("Waiting for bot to come online...")
            time.sleep(10)
        except Exception as e:
            cls.is_chatmember_running = False
            cls.error_msg = str(e)


    @classmethod
    def tearDownClass(cls):
        global CHAT_MEMBER_COMMANDS
        CHAT_MEMBER_COMMANDS.put(ChatMemberCommand(exit=True))
        cls.expect_chatmember_response(lambda message: message.shutdown, timeout=10, error_message="Failed to shutdown bot in time.")
        cls.chat_member_thread.join()
        abort_bot()
        cls.bot_thread.join()
