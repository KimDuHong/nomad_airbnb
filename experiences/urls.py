from django.urls import path
from .views import (
    PerkDetail,
    Perks,
    Experiences,
    ExperienceDetail,
    ExperiencePerk,
    ExperienceBooking,
    ExperienceBookingAll,
    ExperienceBookingDetail,
)

urlpatterns = [
    path("", Experiences.as_view()),
    path("<int:pk>/perks", ExperiencePerk.as_view()),
    path("<int:pk>", ExperienceDetail.as_view()),
    path("<int:pk>/bookings/all", ExperienceBookingAll.as_view()),
    path("<int:pk>/bookings/", ExperienceBooking.as_view()),
    path("<int:pk>/bookings/<int:booking_pk>", ExperienceBookingDetail.as_view()),
    path("perks/", Perks.as_view()),
    path("perks/<int:pk>", PerkDetail.as_view()),
]
