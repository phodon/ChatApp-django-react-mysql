from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['content']  # Tin nhắn từ client
        print(message)

        # Gửi tin nhắn đến room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'content': message
            }
        )

    async def chat_message(self, event):
        message = event['content']
        print(message)

        # Gửi tin nhắn đến WebSocket
        await self.send(text_data=json.dumps({
            'content': message
        }))