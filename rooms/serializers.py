from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from rest_framework import serializers
from reviews.serializers import ReviewSerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomDetailSerializer(ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    # avatar , name , username
    # Many = True 를 하지 않으면 null
    category = CategorySerializer(read_only=True)

    rating = serializers.SerializerMethodField()
    # column 이 아닌 메소드로 만들어진 값을 호출할때,
    is_owner = serializers.SerializerMethodField()
    # 동적 필드
    # reviews = ReviewSerializer(
    #     many=True,
    #     read_only=True,
    # )
    amenities_count = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Room
        exclude = ("amenities",)
        # depth = 1  # 모든 정보가 보임, 커스터마이징이 불가

    def get_rating(self, obj):  # get 을 꼭 붙여야함, obj -> 시리얼라이즈하는 값
        return obj.rating()

    def get_is_owner(self, obj):
        return obj.owner == self.context["request"].user

    def get_reviews_count(self, obj):
        return obj.reviews.count()

    def get_amenities_count(self, obj):
        return obj.amenities.count()


class RoomListSerializer(ModelSerializer):
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "id",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
        )

    def get_rating(self, obj):
        return obj.rating()

    def get_is_owner(self, obj):
        return obj.owner == self.context["request"].user
