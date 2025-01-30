from django.urls import path
from .consumers import OneToOneConsumer

websocket_urlpatterns = [
    path("ws/chatroom/<str:userid>/", OneToOneConsumer.as_asgi(), name = 'one_to_one_consumer'),
]