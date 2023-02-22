from django.db import models
from common.models import CommonModel

# Create your models here.
class Experience(CommonModel):
    country = models.CharField(
        max_length=50,
        default="한국",
    )
    city = models.CharField(
        max_length=80,
        default="서울",
    )
    name = models.CharField(
        max_length=250,
    )
    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    price = models.PositiveIntegerField()
    address = models.CharField(
        max_length=200,
    )
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField(default="")
    perks = models.ManyToManyField(
        "experiences.Perk",
        related_name="experiences",
    )
    category = models.ForeignKey(
        "categories.Category",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="experiences",
    )

    def __str__(self) -> str:
        return self.name


class Perk(CommonModel):

    """what is include on an experience"""

    name = models.CharField(
        max_length=100,
    )
    details = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )
    explanation = models.TextField(
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name
