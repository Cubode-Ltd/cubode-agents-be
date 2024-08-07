from django.urls import re_path, path
from core import consumers

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

websocket_urlpatterns = [
    # re_path(r'ws/agent/$', consumers.DataConsumer.as_asgi()),
    path(r'ws/notifications/', consumers.NotificationConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
