from django.db import models
from common.models import CommonModel

# Create your models here.
class Chatting_Room(CommonModel):
    users = models.ManyToManyField(
        "users.User",
        related_name="chatting_rooms",
    )

    def __str__(self) -> str:
        return "chatting_room"


class Message(CommonModel):
    text = models.TextField()
    user = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="messages",
    )
    room = models.ForeignKey(
        "direct_msgs.Chatting_Room",
        on_delete=models.CASCADE,
        related_name="chatting_rooms",
    )

    def __str__(self) -> str:
        return f"{self.user} : {self.text}"
