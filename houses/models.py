from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class House(AbstractUser):
    
    """HOUSE, 이름, 가격, 설명, 주소"""
    
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    desciption = models.TextField()
    address = models.CharField(max_length=100)