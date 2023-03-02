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
    unread_messages = serializers.SerializerMethodField()

    class Meta:
        model = Chatting_Room
        fields = (
            "id",
            "lastMessage",
            "unread_messages",
            "users",
            "updated_at",
        )

    def get_unread_messages(self, obj):
        # Get the user associated with the request
        user = self.context["request"].user

        # Get the count of unread messages using Django ORM
        num_unread_messages = Message.objects.filter(
            room=obj,
            sender__in=obj.users.exclude(pk=user.pk),
            is_read=False,
        ).count()
        return num_unread_messages


class MessageSerializer(serializers.ModelSerializer):
    sender = TinyUserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = "__all__"
