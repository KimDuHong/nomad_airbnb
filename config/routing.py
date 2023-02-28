from channels.routing import ProtocolTypeRouter, URLRouter

# import app.routing
from django.urls import path

from direct_msgs.consumers import TextRoomConsumer

websocket_urlpatterns = [
    path("ws/<str:room_name>", TextRoomConsumer.as_asgi()),
]
