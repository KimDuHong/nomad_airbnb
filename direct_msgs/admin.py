from django.contrib import admin
from .models import Chatting_Room, Message

# Register your models here.
@admin.register(Chatting_Room)
class Chatting_RoomAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "sender",
        "text",
        "room",
        "created_at",
    )
    list_filter = (
        "room",
        "created_at",
    )
