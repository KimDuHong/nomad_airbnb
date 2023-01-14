from django.contrib import admin
from .models import Room, Amenity


@admin.action(description="set all prices zero")
def reset_all(model_admin, request, rooms):
    for room in rooms:
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    actions = (reset_all,)
    list_display = (
        "name",
        "owner",
        "price",
        "kind",
        "total_amenities",
        "rating",
        "created_at",
    )
    search_fields = (
        "name",
        "price",
    )
    # def total_amenities(self, room):  # 관리자 패널만
    # return room.amenities.count()  # 어메니티의 카운트


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
