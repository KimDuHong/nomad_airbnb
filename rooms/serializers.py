from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from rest_framework import serializers
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "pk",
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
    is_liked = serializers.SerializerMethodField()
    amenities_count = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        exclude = ("amenities",)
        # depth = 1  # 모든 정보가 보임, 커스터마이징이 불가

    def get_rating(self, obj):  # get 을 꼭 붙여야함, obj -> 시리얼라이즈하는 값
        return obj.rating()

    def get_is_owner(self, obj):
        request = self.context.get("request")
        if request:
            return obj.owner == self.context["request"].user
        else:
            return False

    def get_reviews_count(self, obj):
        return obj.reviews.count()

    def get_amenities_count(self, obj):
        return obj.amenities.count()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request:
            if request.user.is_authenticated:
                return Wishlist.objects.filter(
                    user=request.user,
                    rooms__pk=obj.pk,
                ).exists()
        else:
            return False


class RoomListSerializer(ModelSerializer):
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "id",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "reviews_count",
            "is_owner",
            "photos",
        )

    def get_reviews_count(self, obj):
        return obj.reviews.count()

    def get_rating(self, obj):
        return obj.rating()

    def get_is_owner(self, obj):
        request = self.context.get("request")
        if request:
            return obj.owner == self.context["request"].user
        else:
            return False
