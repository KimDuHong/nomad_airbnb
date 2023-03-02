# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer


class TextRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        from .models import Chatting_Room
        from .models import Message
        from users.models import User
        from .serilizers import MessageSerializer
        from users.serializers import TinyUserSerializer

        text_data_json = json.loads(text_data)
        text = text_data_json.get("text")
        sender = text_data_json.get("sender")
        type = text_data_json.get("type")

        room = Chatting_Room.objects.get(pk=self.room_name)
        if not type:
            user = User.objects.get(username=sender)
            self.user = user
            Message.objects.create(text=text, sender=user, room=room)
            user = TinyUserSerializer(user).data

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {"type": "chat_message", "message": text, "sender": user},
            )
            # Update chat list with new last message
            last_message = text
            for user in room.users.all():
                chat_room = user.username + "_notifications"
                async_to_sync(self.channel_layer.group_send)(
                    chat_room,
                    {"type": "new_data", "text": last_message, "room_id": room.id},
                )

    def chat_message(self, event):
        text = event["message"]
        sender = event["sender"]
        self.send(text_data=json.dumps({"text": text, "sender": sender}))


from .models import Message


class NotificationConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.notification_group_name = None

    def connect(self):
        from users.models import User

        user_pk = self.scope["query_string"]
        result = user_pk.decode("utf-8")
        result = result[5:]
        try:
            self.user = User.objects.get(pk=result)
        except User.DoesNotExist:
            return

        # set notification group name
        self.notification_group_name = self.user.username + "_notifications"

        self.accept()

        # add channel to notification group
        async_to_sync(self.channel_layer.group_add)(
            self.notification_group_name,
            self.channel_name,
        )

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.notification_group_name,
            self.channel_name,
        )
        return super().disconnect(code)

    def new_data(self, event):
        self.send_json(event)
