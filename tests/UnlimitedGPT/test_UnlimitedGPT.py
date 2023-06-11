import os
import unittest
from unittest.mock import patch
from src.UnlimitedGPT.UnlimitedGPT import ChatGPT
from src.UnlimitedGPT.internal.objects import ChatGPTResponse, SessionData
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class TestChatGPT(unittest.TestCase):
    def setUp(self):
        self.session_token_1 = os.getenv("SESSION_TOKEN_1")
        self.session_token_2 = os.getenv("SESSION_TOKEN_2")
        self.api = ChatGPT(self.session_token_1)

    def tearDown(self):
        self.api.__del__()
        del self.api

    def test_session_token(self):
        self.assertEqual(self.api._session_token, self.session_token_1)

    def test_send_message_short(self):
        message = self.api.send_message("Hello World.")
        self.assertIsInstance(message, ChatGPTResponse)
        
    def test_send_message_long(self):
        message = self.api.send_message("Write me an essay on AI over 3000 words")
        self.assertIsInstance(message, ChatGPTResponse)

    def test_get_session_data(self):
        session_data = self.api.get_session_data()
        self.assertIsInstance(session_data, SessionData)

    def test_toggle_chat_history_false(self):
        self.api.toggle_chat_history(False)
    
    def test_toggle_chat_history_true(self):
        self.api.toggle_chat_history(True)

    def test_switch_theme(self):
        self.api.switch_theme("DARK")

    def test_clear_conversations(self):
        message = self.api.send_message("Hello World 0.")
        self.api.clear_conversations()
        # Add assertions to check if conversations are cleared

    def test_reset_conversation(self):
        self.api.reset_conversation()
        # Add assertions to check if conversation is reset

    def test_switch_conversation(self):
        message_1 = self.api.send_message("Hello World 1.")
        message_2 = self.api.send_message("Hello World 2.")
        self.api.switch_conversation(message_1.conversation_id)
        message_3 = self.api.send_message("Hello World 3.")
        self.assertEqual(message_1.conversation_id, message_3.conversation_id)

    def test_switch_account(self):
        self.api.switch_account(self.session_token_2)
        message = self.api.send_message("Hello World.")

    def test_logout(self):
        self.api.logout()
        # Add assertions to check if logout is successful

if __name__ == '__main__':
    unittest.main()
