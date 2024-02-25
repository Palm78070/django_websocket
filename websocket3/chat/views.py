from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User

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
	return render(request, "chat/chatroom.html", {
		"room_name" : room_name
	})

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
