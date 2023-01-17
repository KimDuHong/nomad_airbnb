from django.urls import path
from . import views

urlpatterns = [
    path("", views.RoomList.as_view()),
    path("<int:pk>", views.RoomDeatil.as_view()),
    # path("<int:pk>/11",)
    path("amenities/", views.Amenities.as_view()),
    path("amenities/<int:pk>/", views.AmenityDetail.as_view()),
]
