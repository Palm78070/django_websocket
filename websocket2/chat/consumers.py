from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatRoomConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		#scope attribute contains information about the WebSocket connection, including metadata provided by the server, such as the type of connection, the path of the URL, headers, etc.
		#['url_route']: This part of the code accesses a key within the scope dictionary. The url_route key contains information about the URL routing, including any named parameters captured from the URL pattern
		#'kwargs' is another key that holds a dictionary of named URL parameters captured from the URL pattern.
		#This accesses the value of the specific URL parameter named 'room_name'. It's extracting the room name from the URL routing information
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = 'chat_%s' % self.room_name
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name #Contain poiter to channel layer instance
		)

		await self.accept()

		# await self.channel_layer.group_send(
		# 	self.room_group_name,
		# 	{
		# 		"type":"tester_message",
		# 		"tester":"Hello world",
		# 	}
		# )

	# async def tester_message(self, event):
	# 	tester = event["tester"]

	# 	await self.send(text_data=json.dumps({
	# 		"tester":tester,
	# 	}))

	async def disconnect(self, close_code): #use to discard the group
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	async def receive(self, text_data):
		#json.loads() used to deserialize json string into python obj
		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		username = text_data_json['username']

		await self.channel_layer.group_send(
			self.room_group_name,
			{
				"type":"chatroom_message",
				"message":message,
				"username":username,
			}
		)

	async def chatroom_message(self, event):
		message = event['message']
		username = event['username']

		await self.send(text_data=json.dumps({
			"message":message,
			"username":username,
		}))
