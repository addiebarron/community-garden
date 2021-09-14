from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/cursor", consumers.CursorConsumer.as_asgi()),
    path("ws/grid", consumers.GridConsumer.as_asgi()),
    # path("ws/log", consumers.LogConsumer.as_asgi()),
    # path("ws/chat", consumers.ChatConsumer.as_asgi()),
]
