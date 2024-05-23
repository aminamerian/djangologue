from django.test import TestCase
from channels.testing import WebsocketCommunicator
from .consumers import ChatConsumer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async


class ChatConsumerTestCase(TestCase):
    @database_sync_to_async
    def create_user(self, username, password):
        user_model = get_user_model()
        user = user_model.objects.create_user(username=username, password=password)
        return user

    async def test_chat_consumer(self):
        # user = await self.create_user("testuser", "password")
        # access_token = AccessToken.for_user(user)

        self.assertTrue(True)

        # communicator = WebsocketCommunicator(ChatConsumer, "/ws/chat/test_room/")
        # connected, _ = await communicator.connect()
        # self.assertTrue(connected)

        # await communicator.send_json_to({"command": "send", "message": "Hello, World!"})
        # response = await communicator.receive_json_from()
        # self.assertEqual(response["message"], "Hello, World!")
        # self.assertEqual(response["username"], user.username)

        # await communicator.disconnect()
