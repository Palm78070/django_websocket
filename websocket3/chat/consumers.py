from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import ChatRoom, Chat
from django.contrib.auth import get_user_model
from django.utils.html import escape
from django.urls import reverse

User = get_user_model()
user_ch_map = {}

class ChatRoomConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		await self.accept()
		print("Connect to websocket!!!")
		self.room_name = None
		if not self.scope["user"].is_authenticated:
		# Redirect to the login page
			login_url = reverse("login-user")
			redirect_message = {
				"type": "redirect",
				"url": login_url
			}
			#send json string back to cli
			await self.send(text_data=json.dumps(redirect_message))
			await self.close()
			return
		self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

		#syntax of python to insert self.room_name to placeholder %s
		print("After the condition!!!")
		self.room_group_name = "chat_%s" % self.room_name
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)



	async def disconnect(self, close_code):
		#hasattr check if the self obj has the attribute room_group_name
		if hasattr(self, 'room_group_name'):
			await self.channel_layer.group_discard(
				self.room_group_name,
				self.channel_name
			)

	async def save_massage(self, user, sender, message, room):
		# To create and save an object in a single step, use the create() method.
		await database_sync_to_async(Chat.objects.create)(
			user=user,
			room=room,
			# content=user + ": " + message,
			content=f"{sender}: {message}"
		)

	async def get_user_obj(self, username):
		return await database_sync_to_async(User.objects.get)(username=username)  # Get the recipient user object

	async def receive(self, text_data):
		print("In receive function!!!")
		text_data_json = json.loads(text_data)
		message = escape(text_data_json['message'])
		username = text_data_json['username']
		# self.user_id = self.scope['user'].id
		# print("User ID:", self.user_id)  # Print the user_id
		sender = self.scope['user']  # Get the sender user object
		recipient = await self.get_user_obj(text_data_json['recipient'])
		print("User: ", self.scope['user'])
		print("Recipient: ", text_data_json['recipient'])

		#Find room obj
		room = await database_sync_to_async(ChatRoom.objects.get)(name=self.room_name)

		await self.save_massage(sender, sender, message, room)
		await self.save_massage(recipient, sender, message, room)

		#Save message for sender
		# await database_sync_to_async(Chat.objects.create)(
		# 	user=sender,
		# 	room=room,
		# 	# content=sender + ": " + message,
		# 	content=f"{sender}: {message}"
		# )

		#Save message for recipient
		# await database_sync_to_async(Chat.objects.create)(
		# 	user=recipient,
		# 	room=room,
		# 	# content=recipient + ": " + message,
		# 	content=f"{sender}: {message}"
		# )

		await self.channel_layer.group_send(
			self.room_group_name,
			{
				"type" : "chat_message",
				"message" : message,
				"username" : username,
			}
		)

	async def chat_message(self, event):
		message = event['message']
		username = event['username']

		print(f"consumers.py => Received message from {username}: {message}")

		await self.send(text_data=json.dumps({
			"message" : message,
			"username" : username,
		}))
