# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from api.models import Profile, Workspaces
from api.workspaces.serializers import WorkspaceSerializer
from asgiref.sync import sync_to_async


class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        self.room_group_name = f'user_{user.id}'
        if user.is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

            profile = await Profile.objects.aget(user=user)
            workspaces = Workspaces.objects.filter(members=profile)
            serializer = WorkspaceSerializer(workspaces, many=True)
            await self.send(text_data=json.dumps({
                'workspace_members': await sync_to_async(lambda: serializer.data)(),
                'workspace_member_orders': profile.workspace_member_orders,
            }))
    
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
            'workspace_member_orders': workspace_member_orders,
        }))
        