from rest_framework.serializers import ModelSerializer
from .models import User
from rest_framework import serializers


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "avatar",
            "name",
            "username",
        )


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "email",
            "password",
            "is_superuser",
            # "id",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        )


class PublicUserSerializer(ModelSerializer):
    have_rooms = serializers.SerializerMethodField()
    have_reviews = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "name",
            "avatar",
            "gender",
            "language",
            "currency",
            "have_rooms",
            "have_reviews",
        )

    def get_have_rooms(self, obj):
        return obj.rooms.count()

    def get_have_reviews(self, obj):
        return obj.reviews.count()
