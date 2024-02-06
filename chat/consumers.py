import json
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

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
		self.accept() #accepts the WebSocket connection

		#sends a message to the client immediately after the connection is established.
		#sends a JSON-formatted message
		self.send(text_data=json.dumps({
			'type':'connection_established',
			'message':'You are now connected!!'
		}))
