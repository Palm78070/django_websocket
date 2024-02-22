"""
ASGI config for websocket3 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
# from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websocket3.settings")

# application = get_asgi_application()
application = ProtocolTypeRouter({
	"http" : get_asgi_application(),
	"websocket" : AuthMiddlewareStack(
		URLRouter(
			chat.routing.websocket_urlpatterns
		)
	),
})
