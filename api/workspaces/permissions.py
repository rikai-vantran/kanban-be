from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from api.models import WorkspaceMembers

class IsOwnerWorkspacePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        workspace_id = request.parser_context['kwargs']['workspace_id']
        if not WorkspaceMembers.objects.filter(workspace_id=workspace_id, role='owner', member__user=request.user).exists():
            return False
        return True