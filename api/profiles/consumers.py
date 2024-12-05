# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['uid']
        self.room_group_name = f"user_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_new_workspace_members(self, event):
        workspace_members = event['workspace_members']
        workspace_member_orders = event['workspace_member_orders']
        await self.send(text_data=json.dumps({
            'workspace_members': workspace_members,
            'workspace_member_orders': workspace_member_orders
        }))
        