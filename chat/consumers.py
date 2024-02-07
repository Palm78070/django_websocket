import json
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

# class ChatConsumer(AsyncWebsocketConsumer):
# 	async def connect(self): #used to define an asynchronous function in Python
# 		await self.accept() #accepts the WebSocket connection

# 		#sends a message to the client immediately after the connection is established.
# 		#sends a JSON-formatted message
# 		await self.send(text_data=json.dumps({
# 			'type':'connection_established',
# 			'message':'You are now connected!!'
# 		}))

class ChatConsumer(WebsocketConsumer):
	def connect(self): #Called when connection is established
		self.room_group_name = 'test' #Var that store group name

		#use the following function to add group and add user channel to group
		#group_add is an asynchronous function and may not be compatible with synchronous code, async_to_sync is used to convert it to synchronous cod
		async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name
		)

		self.accept() #accepts the WebSocket connection

		#sends a message to the client immediately after the connection is established.
		#sends a JSON-formatted message
		# self.send(text_data=json.dumps({
		# 	'type':'connection_established',
		# 	'message':'You are now connected!!'
		# }))

	def receive(self, text_data): #Called when receive msg from cli
		#parse text_data(JSON format) into Python dict obj => use json.loads to convert json => dict obj
		text_data_json = json.loads(text_data)

		#retrieves the value associated with message key
		#assumes that the received JSON data contains a key named 'messageee'
		message = text_data_json['message']

		# print('Message:', message)

		#send msg back to cli whenever we receive msg fro cli
		# self.send(text_data=json.dumps({
		# 	'type':'chat',
		# 	'message':message
		# }))

		#This function is used to send a message to all consumers in a particular group
		async_to_sync(self.channel_layer.group_send)(
			self.room_group_name,
			{
				#Dict that tells type and function to send
				'type':'chat_message',
				'message':message #includes the actual content of the message that is being sent to the group of consumers, will be parse to chat_message funct. through event
			}
		)

	#When the msg of type 'chat_message' is received by consumers, the chat_message function is invoke
	def chat_message(self, event):
		message = event['message']

		self.send(text_data=json.dumps({
			'type':'chat',
			'message':message
		}))
