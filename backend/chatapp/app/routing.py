from django.urls import re_path
from . import consumer

websocket_urlpatterns = [
    # Định tuyến WebSocket cho consumer
    re_path(r"ws/chat/", consumer.ChatConsumer.as_asgi()), 
]