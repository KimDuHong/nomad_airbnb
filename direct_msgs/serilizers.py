from rest_framework import serializers
from .models import Chatting_Room, Message
from users.serializers import TinyUserSerializer


class ChatListSerializer(serializers.ModelSerializer):
    sender = TinyUserSerializer()

    class Meta:
        model = Message
        exclude = (
            "id",
            "room",
            "updated_at",
        )


class ChatRoomListSerializer(serializers.ModelSerializer):
    users = TinyUserSerializer(read_only=True, many=True)
    # last_message = ChatListSerializer()

    class Meta:
        model = Chatting_Room
        fields = (
            "id",
            "lastMessage",
            "users",
            "updated_at",
        )


class MessageSerializer(serializers.ModelSerializer):
    sender = TinyUserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = "__all__"
