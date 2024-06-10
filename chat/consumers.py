import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Messages
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.room_name = None
        self.room_group_name = None
        self.user = None
        self.usermodel = None

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"].username or "Anonymous"
        self.usermodel = self.scope["user"]

        # join room group
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @database_sync_to_async
    def save_message(self, message, user, room_name):
        room = ChatRoom.objects.get(name=room_name)
        Messages.objects.create(message=message, user=user, room=room)    

    async def receive(self, text_data=None, bytes_data=None):
        # load text_data   that come from response
        text_data_json = json.loads(text_data)

        #get message from text_data_json
        message = text_data_json['message']

        # save Message in db
        await self.save_message(message, self.usermodel, self.room_name)


        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "send_message", "message":message, "username": self.user},

        )


    async def send_message(self, event):
        message = event["message"]
        username = event["username"]

        await self.send(
            text_data=json.dumps({"message": message, "username": username})
        )    