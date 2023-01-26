from rest_framework.serializers import ModelSerializer
from .models import Perk, Experience
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer, CategoryNameSerializer
from rest_framework import serializers


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class ExperienceSerializer(ModelSerializer):
    category = CategoryNameSerializer(read_only=True)

    class Meta:
        model = Experience
        fields = (
            "name",
            "start",
            "end",
            "country",
            "category",
        )


class ExperienceDetailSerializer(ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    perks_count = serializers.SerializerMethodField()
    bookings_count = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        exclude = ("perks",)

    def get_perks_count(self, obj):
        return obj.perks.count()

    def get_bookings_count(self, obj):
        return obj.bookings.count()
