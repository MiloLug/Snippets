from django.urls import re_path

from some_app import consumers

websocket_urlpatterns = [
    re_path(r'ws/some_app/$', consumers.SomeConsumer.as_asgi()),
]
