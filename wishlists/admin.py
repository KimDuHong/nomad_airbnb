from django.contrib import admin
from .models import Wishlist

# Register your models here.
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "name",
        "created_at",
        "updated_at",
    )
