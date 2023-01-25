from django.urls import path
from .views import (
    Me,
    Users,
    PublicUser,
    ChangePassword,
    LogIn,
    LogOut,
    PublicUserReviews,
    PublicUserRooms,
)

urlpatterns = [
    path("me", Me.as_view()),  # get
    path("", Users.as_view()),  # post
    path("@<str:username>", PublicUser.as_view()),  # get
    path("@<str:username>/reviews", PublicUserReviews.as_view()),  # get
    path("@<str:username>/rooms", PublicUserRooms.as_view()),  # get
    path("log-in", LogIn.as_view()),  # post
    path("log-out", LogOut.as_view()),  # post
    path("change-password", ChangePassword.as_view()),  # put
]
