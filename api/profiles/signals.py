from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from api.models import Workspaces
from api.workspaces.serializers import WorkspaceSerializer

@receiver(post_save, sender=Profile)
def profile_workspace_members_order_changed(sender, instance, created, **kwargs):
    if created:
        return
    workspace_member_orders_old = instance.get_dirty_fields().get('workspace_member_orders')
    workspace_member_orders_new = instance.workspace_member_orders

    if workspace_member_orders_old is None or workspace_member_orders_new is None:
        return
    if workspace_member_orders_old.count != workspace_member_orders_new.count:
        uid = User.objects.get(profile=instance).id
        channel_layer = get_channel_layer()

        workspaces = Workspaces.objects.filter(workspacemembers__role='member')
        serializer = WorkspaceSerializer(workspaces, many=True)
        async_to_sync(channel_layer.group_send)(
            f'user_{uid}',
            {
                'type': 'send_new_workspace_members',
                'workspace_members': serializer.data,
                'workspace_member_orders': workspace_member_orders_new,
            }
        )