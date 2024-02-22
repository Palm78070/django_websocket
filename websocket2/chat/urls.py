from django.urls import path
from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("<str:room_name>/", views.room, name="room"),
]
#<str:room_name> => syntax of django used as a placeholder to capture specific str from url
#the room_name will be passed as argument to view.py
