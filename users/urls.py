from django.urls import path
from .views import Me, Users, PublicUser, ChangePassword, LogIn, LogOut

urlpatterns = [
    path("me", Me.as_view()),
    path("", Users.as_view()),
    path("@<str:username>", PublicUser.as_view()),
    path("log-in", LogIn.as_view()),
    path("log-out", LogOut.as_view()),
    path("change-password", ChangePassword.as_view()),
]
