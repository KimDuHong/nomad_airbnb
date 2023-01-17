from rest_framework.views import APIView
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomDetailSerializer, RoomListSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from django.db import transaction

# GET /api/v1/rooms
# GET POST /api/v1/rooms/amenities
# GET PUT DELETE /api/v1/rooms/amenities/1


class RoomDeatil(APIView):
    def is_negative(self, value):
        if value:
            if value < 0:
                return True
        return False

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data)

    def put(self, request, pk):
        if not request.user.is_authenticated:
            raise NotAuthenticated  # 자격 인증 데이터
        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied  # 권한
        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            # ------check NEGATIVE VALUE ------------------------

            price = request.data.get("price")
            if self.is_negative(price):
                raise ParseError("negative price")
            rooms = request.data.get("rooms")
            if self.is_negative(rooms):
                raise ParseError("negative rooms_count")
            toilets = request.data.get("toilets")
            if self.is_negative(toilets):
                raise ParseError("negative toilets_count")

            # ------check AMENITY ------------------------

            amenities_pk = request.data.get("amenities")
            if amenities_pk:
                room.amenities.clear()
                for pk in amenities_pk:
                    try:
                        amenity = Amenity.objects.get(pk=pk)
                        room.amenities.add(amenity)
                    except Amenity.DoesNotExist:
                        raise ParseError("Invalid Amenity pk")

            # ------check CATEGORY ------------------------

            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError(f"Must Be Rooms")
                    room.category = category
                except Category.DoesNotExist:
                    raise ParseError("Invalid Category pk")

            update_room = serializer.save()
            return Response(RoomDetailSerializer(update_room).data)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            raise NotAuthenticated  # 자격 인증 데이터
        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied  # 권한
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomList(APIView):
    def get(self, request):
        all_room = Room.objects.all()
        serializer = RoomListSerializer(all_room, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:  # 로그인 체크
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("Need category, category is required")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms'")
                except Category.DoesNotExist:
                    raise ParseError("Category Not Found")
                try:
                    with transaction.atomic():
                        # transaction - > 모든 쿼리를 한번에, 에러가 발생하면 no commit
                        # 카 테고리 데이터를 필수로 받는다, 카테고리 id를 인자로 받아서 처리
                        room = serializer.save(
                            owner=request.user,
                            category=category,
                        )
                        # create method call, owner defined
                        amenities = request.data.get("amenities")
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                            # raise ParseError(f"Amenity Not Found, id {amenity_pk} is not")
                    # amenity is Many to Many field, so we need to add
                except Exception:
                    raise ParseError(f"Amenity Not Found, id {amenity_pk} is not")

                serializer = RoomDetailSerializer(room)
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(id=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,  ## 부분적 업데이트
        )
        if serializer.is_valid():
            update_amenity = serializer.save()
            return Response(AmenitySerializer(update_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=204)
