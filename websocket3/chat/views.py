from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView

# class CustomLoginView(LoginView):
#     def get_success_url(self):
#         # Check if 'next' parameter exists in the query string
#         next_url = self.request.GET.get('next')
#         if next_url:
#             return next_url
#         # Default URL to redirect after login if 'next' parameter is not present
#         return super().get_success_url()

from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from urllib.parse import urlparse, parse_qs

class CustomLoginView(LoginView):
	def get_success_url(self):
		# Get the 'next' parameter from the query string
		next_url = self.request.GET.get('next')

		if next_url:
			# Parse the next URL to extract the room name
			parsed_url = urlparse(next_url)
			query_params = parse_qs(parsed_url.query)
			room_name = query_params.get('room', [''])[0]  # Get the value of 'room' parameter

			if room_name:
				# Redirect to the specific room after successful login
				return next_url

		# If no specific room is specified, use the default success URL
		return super().get_success_url()


# Create your views here.
def index(request):
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
