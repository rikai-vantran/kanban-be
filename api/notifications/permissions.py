from rest_framework import permissions
from api.notifications.models import Request

# class IsOwnerWorkspacePermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         workspace_id = request.parser_context['kwargs']['workspace_id']
#         print('workspace_id', workspace_id)
#         if not WorkspaceMembers.objects.filter(workspace_id=workspace_id, role='owner', member__user=request.user).exists():
#             return False
#         return True

class IsUserReceiverPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        request_id = request.parser_context['kwargs']['request_id']
        requestNotification = Request.objects.get(id=request_id)
        if request.user.profile != requestNotification.user_receiver:
            return False
        return True