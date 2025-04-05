import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from dinar.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(websocket_urlpatterns),
})
