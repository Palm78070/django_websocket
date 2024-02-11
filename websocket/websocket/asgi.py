"""
ASGI config for websocket project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter #imports the ProtocolTypeRouter, URLRouter class from the channels.routing module
#ProtocolTypeRouter is a router provided by Django Channels that allows you to route different protocols to different ASGI applications or handlers

#AuthMiddlewareStack is a middleware provided by Django Channels that handles authentication for WebSocket connections
#It intercepts incoming WebSocket connections and can perform operations like authentication, authorization, and message processing before passing the connection to the appropriate consumer.
from channels.auth import AuthMiddlewareStack

from channels.security.websocket import AllowedHostsOriginValidator

import chat.routing #import routing module from chat package
#chat.routing module likely contains the URL routing configuration for WebSocket connections in your Django Channels application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websocket.settings")

#Change value of application to newly import ProtocolTypeRouter

#application = ProtocolTypeRouter({...}): This line creates an instance of the ProtocolTypeRouter class, passing a dictionary as an argument

#In this dictionary, each key represents a protocol, and the corresponding value is the ASGI application or handler to which requests of that protocol should be routed

#get_asgi_application() is a utility function provided by Django that returns the ASGI application for handling HTTP requests in a Django project

application = ProtocolTypeRouter({
	#'http' defines the routing for HTTP connections. It routes all incoming HTTP requests to the default ASGI application for handling HTTP requests
	#'websocket' defines the routing for WebSocket connections => wraps the URLRouter to apply authentication middleware to WebSocket connections
	'http':get_asgi_application(),
	'websocket':AuthMiddlewareStack(
		URLRouter(
			chat.routing.websocket_urlpatterns #contains a list of URL patterns and their corresponding consumer classes for WebSocket connections
		)
	)
})
