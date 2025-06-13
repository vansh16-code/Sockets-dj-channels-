import json
import urllib.parse
from channels.generic.websocket import AsyncWebsocketConsumer

# In-memory store for active users per room (not for production!)
active_users = {}  # { room_name: set of names }

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Room and user setup
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Parse user name from query params
        query_string = self.scope["query_string"].decode()
        params = urllib.parse.parse_qs(query_string)
        self.name = params.get("name", ["Anonymous"])[0]

        # Track active users
        if self.room_name not in active_users:
            active_users[self.room_name] = set()
        active_users[self.room_name].add(self.name)

        # Join channel group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Notify join and send updated user list
        await self.send_user_update(f"🔔 {self.name} has joined the chat!")

    async def disconnect(self, close_code):
        # Remove user from tracking
        if self.room_name in active_users:
            active_users[self.room_name].discard(self.name)
            if not active_users[self.room_name]:
                del active_users[self.room_name]

        # Leave group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # Notify leave and update user list
        await self.send_user_update(f"👋 {self.name} has left the chat.")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = f"{self.name}: {data.get('message', '')}"
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.message", "message": message}
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "users": list(active_users.get(self.room_name, []))
        }))

    async def send_user_update(self, announcement):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": announcement
            }
        )
