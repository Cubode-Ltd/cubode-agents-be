# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class DataConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
from datetime import datetime

class DataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.user = self.scope['user']
        # if self.user.is_authenticated: # Cookies session based authentication.
        await self.accept()
        await self.channel_layer.group_add("agent_tasks", self.channel_name) # Add to group to send messages later

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("agent_tasks", self.channel_name)


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json.get('type') == 'ping':
            await self.send(text_data=json.dumps({'type': 'pong'}))
        else:
            message = text_data_json['message']
            await self.channel_layer.group_send(
                "chat",
                {
                    'type': 'agent_message',
                    'message': json.dumps(message)
                }
            )

    # async def send_time(self):
    #     while True:
    #         await self.send(text_data=json.dumps({
    #             'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #         }))
    #         await asyncio.sleep(2)

    # async def send_data(self, message):
    #     await self.send(text_data=json.dumps(message))

    async def agent_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))