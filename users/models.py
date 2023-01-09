from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        Female = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")

    class CurrencyChoices(models.TextChoices):
        WON = "won", "korean Won"
        USD = "usd", "Dollar"

    first_name = models.CharField(
        max_length=100,
        editable=False,
    )
    last_name = models.CharField(
        max_length=100,
        editable=False,
    )
    name = models.CharField(
        max_length=100,
        default="",
    )
    is_host = models.BooleanField(
        null=True,
    )
    avatar = models.ImageField(
        null=True,
        blank=True,
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
    )
    currency = models.CharField(
        max_length=5,
        choices=CurrencyChoices.choices,
    )
