from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
	#r'' => get raw string / will be treat as normal str
	#?P<>pattern => refer to matched str through its name => We extract it from url to use in consumer.py
	#\w+ => pattern to match one or more word char
	#as_asgi => returns an ASGI wrapper application that will instantiate a new consumer instance for each connection or scope
	re_path(r'ws/chat/room/(?P<room_name>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),
]
