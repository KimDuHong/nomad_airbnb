from django.db import models
from common.models import CommonModel

# Create your models here.
class Photo(CommonModel):

    file = models.URLField()
    description = models.CharField(
        max_length=140,
    )
    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="photos",
    )

    def __str__(self):
        return f"photo : {self.file}"


class Video(CommonModel):
    file = models.URLField()

    experience = models.OneToOneField(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="videos",
    )

    def __str__(self) -> str:
        return f"video : {self.file}"
