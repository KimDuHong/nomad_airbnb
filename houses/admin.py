from django.contrib import admin
from .models import House

# Register your models here.
@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ("name", "price_per_night", "address", "is_pet_allow")
    list_filter = ("is_pet_allow",)
