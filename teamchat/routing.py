from django.urls import path
from .consumers import OneToOneConsumer, GroupConsumer

websocket_urlpatterns = [
    path("ws/chatroom/personal/<str:userid>/", OneToOneConsumer.as_asgi(), name = 'one_to_one_consumer'),
    path("ws/chatroom/group/<str:groupid>/", GroupConsumer.as_asgi(), name = 'group_consumer'),
]