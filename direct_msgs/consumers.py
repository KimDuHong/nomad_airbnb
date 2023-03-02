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
            room_id = self.room_name

            print(self.user.username + "__notifications")
            async_to_sync(self.channel_layer.group_send)(
                "__notifications",
                {"type": "unread_count", "message": 1, "room_id": 1},
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

        self.accept()

        # private notification group
        self.notification_group_name = "__notifications"
        async_to_sync(self.channel_layer.group_add)(
            self.notification_group_name,
            self.channel_name,
        )
        # print("__notifications")

        # # Send count of unread messages
        # # unread_count = Message.objects.filter(user=self.user).count()
        # self.send_json(
        #     {
        #         "type": "unread_count",
        #         "1": 1,
        #     }
        # )

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.notification_group_name,
            self.channel_name,
        )
        return super().disconnect(code)

    def new_message_notification(self, event):
        self.send_json(event)

    def unread_count(self, event):
        self.send_json(event)
