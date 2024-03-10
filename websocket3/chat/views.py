from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import ChatRoom, Chat

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# Create your views here.
def index(request):
	print("!!! In index function !!!")
	if not request.user.is_authenticated:
		return redirect("login-user")
	print("!!! user is authenticated !!!")
	return render(request, "chat/index.html")

def redirect_to_room(request, room_name):
	print("\nIn redirect_to_room!!!\n")
	if request.user.is_authenticated:
		return render(request, "chat/chatroom.html", {
		"room_name" : room_name
	})
	else:
		return redirect("login-user")

def room(request, room_name):
	print("!!! In room function !!!")
	if not request.user.is_authenticated:
		return redirect("login-user")

	#Queries db for a ChatRoom obj with the specified room_name
	#If found, room will contain the first matching ChatRoom obj, If not found, it will be None
	room = ChatRoom.objects.filter(name=room_name).first()
	chats = []

	if room: #If a room is found in db => Fetches all Chat obj associated with that room
		chats = Chat.objects.filter(room=room)
	else: #If room not found, Creates a new ChatRoom obj with the given room_name + save obj in db
		room = ChatRoom(name=room_name)
		room.save()

	return render(request, "chat/chatroom.html", {
		"room_name" : room_name,
		"chats" : chats
	})

# def room(request, room_name):
# 	print("!!! In room function !!!")
# 	if not request.user.is_authenticated:
# 		return redirect("login-user")
# 	return render(request, "chat/chatroom.html", {
# 		"room_name" : room_name
# 	})

def get_user_list(request):
	print("\n!!!In get_user_list function!!!\n")
	#Check if user that request is authenticate?
	if request.user.is_authenticated:
		#query db to get list of username by using ORM to interact with db
		#exclude() filter out current auth user
		#value_lists() get only username field => flat=True flattens the result into single list
		users = User.objects.exclude(username=request.user.username).values_list('username', flat=True)
		#Convert query set of username into python list
		user_list = list(users)
		# Use JsonResponse class to return list of username
		return JsonResponse({'user_list' : user_list})
		# return JsonResponse({'user_list' : users})
	else:
		return JsonResponse({'error' : 'User not authenticated'})

def send_message(request):
	print("\n!!!In send_message!!!\n")
	if not request.user.is_authenticated:
		print("\nUser is not authenticated\n")
		return JsonResponse({'error': 'User is not authenticated'}, status=401)

	if request.method == 'POST':
		#json.loads() used to deserialize json string into python obj
		data = json.loads(request.body)
		message = data.get('message')
		username = data.get('username')
		room_name = data.get('room_name')  # Make sure to include the room name in the request

		print(f"views.py => Room name: {room_name} => {username}: {message}")

		# Broadcast the message to the WebSocket room
		channel_layer = get_channel_layer()
		#Because view function is synchronous => we have to change it to sync first
		async_to_sync(channel_layer.group_send)(
			f"chat_{room_name}",
			{
				"type": "chat.message",
				"message": message,
				"username": username
			}
		)

		return JsonResponse({'status': 'Message sent successfully'})
	else:
		return JsonResponse({'error': 'Invalid request method'}, status=400)
