from rest_framework import permissions
from rest_framework.response import Response
from api.models import WorkspaceMembers

class IsOwnerWorkspacePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        workspace_id = request.parser_context['kwargs']['workspace_id']
        print('workspace_id', workspace_id)
        if not WorkspaceMembers.objects.filter(workspace_id=workspace_id, role='owner', member__user=request.user).exists():
            return False
        return True

class IsMemberWorkspacePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        workspace_id = request.parser_context['kwargs']['workspace_id']
        if not WorkspaceMembers.objects.filter(workspace_id=workspace_id, member__user=request.user, role='member').exists():
            return False
        return True

class IsOwnerOrMemberWorkspacePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        workspace_id = request.parser_context['kwargs']['workspace_id']
        print('workspace_id', workspace_id)
        if not WorkspaceMembers.objects.filter(workspace_id=workspace_id, member__user=request.user).exists():
            return False
        return True