from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from core.models import Room, Membership, MembershipStatus


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_group_name = None

        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
        else:
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            self.room, created = await self._get_or_create_room(
                self.room_name, self.user
            )
            if await self._is_user_authorized(self.user, self.room, created):
                self.room_group_name = f"chat_{self.room_name}"
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name,
                )
                await self.accept()
            else:
                await self.close()

    async def disconnect(self, close_code):
        if self.room_group_name is not None:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name,
            )

    async def receive_json(self, content):
        command = content.get("command", None)
        if command in [
            "send",
        ]:
            message = await self._save_chat_message(
                self.room, self.user, content["message"]
            )
            await self._send_chat_message(message)

    @database_sync_to_async
    def _get_or_create_room(self, room_name, user):
        room, created = Room.objects.get_or_create(
            name=room_name, defaults={"created_by": user}
        )
        if created:
            Membership.objects.create(
                user=user, room=room, status=MembershipStatus.CONFIRMED
            )
        else:
            Membership.objects.get_or_create(user=user, room=room)
        return room, created

    @database_sync_to_async
    def _is_user_authorized(self, user, room, is_room_created):
        """
        Whether the user is authorized to connect to the chat room.
        """
        if is_room_created:
            return True

        return Membership.objects.filter(
            user=user,
            room=room,
            status=MembershipStatus.CONFIRMED,
        ).exists()

    async def _send_chat_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "id": message.id,
                "content": message.content,
                "created_at": message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "creator_username": self.user.username,
                "creator_email": self.user.email,
            },
        )

    async def chat_message(self, event):
        await self.send_json(
            {
                "id": event["id"],
                "content": event["content"],
                "created_at": event["created_at"],
                "creator_username": event["creator_username"],
                "creator_email": event["creator_email"],
            }
        )

    @database_sync_to_async
    def _save_chat_message(self, room, user, content):
        return room.messages.create(user=user, content=content)
