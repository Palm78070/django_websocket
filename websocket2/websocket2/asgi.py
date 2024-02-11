"""
ASGI config for websocket2 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websocket2.settings")

application = get_asgi_application()

# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# import chat.routing

# application = ProtocolTypeRouter({
# 	"websocket":AuthMiddlewareStack(
# 		URLRouter(
# 			chat.routing.websocket_urlpatterns
# 		)
# 	),
# })
