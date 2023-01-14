from django.urls import path
from . import views

# urlpatterns = [
#     path("", views.Categories.as_view()),
#     path("<int:pk>", views.CategoryDetail.as_view()),
# ]

urlpatterns = [
    path(
        "",
        views.CategoryViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "<int:pk>",
        views.CategoryViewSet.as_view(
            {
                "get": "retrieve",
                "put": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
]
