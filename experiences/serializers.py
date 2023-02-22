from rest_framework.serializers import ModelSerializer
from .models import Perk, Experience
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer, CategoryNameSerializer
from rest_framework import serializers
from django.utils import timezone


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class ExperienceSerializer(ModelSerializer):
    category = CategoryNameSerializer(read_only=True)
    host = TinyUserSerializer(read_only=True)
    perks_count = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = (
            "id",
            "name",
            "perks_count",
            "host",
            "category",
            "start",
            "end",
        )

    def get_perks_count(self, obj):
        return obj.perks.count()


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

    def validate_price(self, value):
        if value >= 0:
            return value
        else:
            raise serializers.ValidationError("price is nagative")

    def validate_start(self, value):
        now = timezone.localtime(timezone.now()).time()
        if value < now:
            raise serializers.ValidationError(
                "Start time must be later than the current time"
            )
        else:
            return value

    def validate_end(self, value):
        now = timezone.localtime(timezone.now()).time()
        if value < now:
            raise serializers.ValidationError("End time is earlier than current time.")
        else:
            return value

    # 특정 필드가 아닌 validator 자체에서 띄우는 에러
    def validate(self, value):
        if value["start"] >= value["end"]:
            raise serializers.ValidationError("End time is earlier than start time.")
        else:
            return value
