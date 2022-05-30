import os

from main_app.wsgi import *

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from some_app import routing as some_app_routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main_app.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            some_app_routing.websocket_urlpatterns
        )
    ),
})
