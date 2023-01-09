from django.db import models

# Create your models here.
class House(models.Model):

    """HOUSE, 이름, 가격, 설명, 주소"""

    name = models.CharField(max_length=100)
    price_per_night = models.PositiveIntegerField()
    desciption = models.TextField()
    address = models.CharField(max_length=100)
    is_pet_allow = models.BooleanField(
        default=True,
        help_text="반려동물 여부를 확인해주세요",
        verbose_name="반려동물이 함께하나요?",
    )
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    category = models.ForeignKey(
        "categories.Category",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self) -> str:
        return self.name
