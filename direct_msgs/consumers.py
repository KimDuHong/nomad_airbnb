# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class TextRoomConsumer(WebsocketConsumer):
    def connect(self):
        # gets 'room_name' and open websocket connection
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]  #
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        from .models import Chatting_Room
        from .models import Message
        from users.models import User
        from .serilizers import MessageSerializer

        text_data_json = json.loads(text_data)
        text = text_data_json.get("text")
        sender = text_data_json.get("sender")
        type = text_data_json.get("type")
        # Send message to room group
        room = Chatting_Room.objects.get(pk=self.room_name)
        if not type:
            user = User.objects.get(username=sender)
            Message.objects.create(text=text, user=user, room=room)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {"type": "chat_message", "message": text, "sender": sender},
            )
        elif type == "loadChatHistory":
            message = Message.objects.filter(room=room)
            serializer = MessageSerializer(message, many=True)
            for i in reversed(serializer.data):
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        "type": "chat_message",
                        "message": i.get("text"),
                        "sender": i.get("user").get("username"),
                    },
                )

    def chat_message(self, event):
        # Receive message from room group
        text = event["message"]
        sender = event["sender"]
        self.send(text_data=json.dumps({"text": text, "sender": sender}))
