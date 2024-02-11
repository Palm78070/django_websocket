from django.urls import re_path #used to define regular expression-based URL patterns
from . import consumers

websocket_urlpatterns = [
	#r'ws/socket-server': This regular expression pattern matches WebSocket connections with a path starting with 'ws/socket-server'
	re_path(r'ws/socket-server', consumers.ChatConsumer.as_asgi()) #.asgi() used to convert consumer class into an ASGI app instance
]
