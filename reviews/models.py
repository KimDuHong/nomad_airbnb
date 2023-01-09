from django.db import models
from common.models import CommonModel

# Create your models here.
class Review(CommonModel):
    """review from a User to a Room Experience"""

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,  # 유저 삭제 -> 리뷰도 삭제
    )
    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    payload = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.user} 님의 별점 : {self.rating}"
