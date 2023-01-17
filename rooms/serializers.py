from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


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
    amenities = AmenitySerializer(many=True, read_only=True)
    # Many = True 를 하지 않으면 null
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Room
        fields = "__all__"
        # depth = 1  # 모든 정보가 보임, 커스터마이징이 불가


class RoomListSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "id",
            "name",
            "country",
            "city",
            "price",
        )
