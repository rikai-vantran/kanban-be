from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import WorkspaceSerializer, WorkspaceInfoSerializer, WorkspaceLabelSerializer
from drf_yasg.utils import swagger_auto_schema
from api.models import Workspaces, Profile
from api.workspaces.permissions import IsOwnerWorkspacePermission, IsOwnerOrMemberWorkspacePermission, IsMemberWorkspacePermission
from api.models import Request, WorkspaceLabels
from api.notifications.serializers import RequestSerializer


class WorkspaceListView(APIView):
    permission_classes = [IsAuthenticated]

    # Create a new workspace
    @swagger_auto_schema(request_body=WorkspaceSerializer)
    def post(self, request):
        serializer = WorkspaceSerializer(data=request.data)
        if serializer.is_valid():
            # Create a new workspace
            workspace = Workspaces.objects.create(
                name=serializer.validated_data['name'],
                icon_unified=serializer.validated_data['icon_unified'],
                column_orders=[]
            )
            # Add workspace to the user's workspaces with role owner
            profile = Profile.objects.get(user=request.user)
            workspace.members.add(profile, through_defaults={"role": 'owner'})

            # update workspace_owner_orders of the owner
            profile.workspace_owner_orders.append(str(workspace.id))
            profile.save()

            return Response({
                "message": "Workspace created successfully",
                "data": WorkspaceSerializer(workspace).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Get all workspaces of the user
    def get(self, request):
        role = request.query_params.get('role')
        if role == 'member':
            workspaces = Workspaces.objects.filter(workspacemembers__role='member', workspacemembers__member__user=request.user)
        elif role == 'owner':
            workspaces = Workspaces.objects.filter(workspacemembers__role='owner', workspacemembers__member__user=request.user)
        elif role:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = WorkspaceInfoSerializer(workspaces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class WorkspaceOwnerDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerWorkspacePermission]

    # Delete a workspace by id
    def delete(self, request, workspace_id):
        workspace = Workspaces.objects.get(id=workspace_id)
        # update workspace_member_orders of all members
        for member in workspace.members.filter(workspacemembers__role='member'):
            profile = Profile.objects.get(user=member.user)
            profile.workspaces_set.remove(workspace_id)
            profile.workspace_member_orders.remove(workspace_id)
            profile.save()
        # update workspace_owner_orders of the owner
        try:
            profile = Profile.objects.get(user=request.user)
            profile.workspace_owner_orders.remove(workspace_id)
            profile.save()
        except:
            pass
        # delete workspace
        workspace.delete()
        return Response({"message": "Workspace deleted successfully"}, status=status.HTTP_200_OK)

    # Update a workspace by id
    def put(self, request, workspace_id):
        workspace = Workspaces.objects.get(id=workspace_id)
        serializer = WorkspaceSerializer(workspace, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Workspace updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WorkspaceDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrMemberWorkspacePermission]

    # Get Workspace by id
    def get(self, request, workspace_id):
        workspace = Workspaces.objects.get(id=workspace_id)
        serializer = WorkspaceSerializer(workspace)
        return Response(serializer.data, status=status.HTTP_200_OK)

class WorkspaceMemberListView(APIView):
    permission_classes = [IsAuthenticated, IsMemberWorkspacePermission]

    # Remove current user from a workspace
    def delete(self, request, workspace_id):
        # get workspace and profile
        workspace = Workspaces.objects.get(id=workspace_id)
        profile = Profile.objects.get(user=request.user)
        # check if the user is the owner of the workspace
        if not workspace.members.filter(workspacemembers__role='owner', workspacemembers__member__user=request.user).exists():
            # remove the user from the workspace
            workspace.members.remove(profile)
            # update workspace_member_orders of the user
            profile.workspaces_set.remove(workspace_id)
            profile.workspace_member_orders.remove(workspace_id)
            profile.save()
            return Response({"message": "You have left the workspace"}, status=status.HTTP_200_OK)
        return Response({"error": "You can't leave the workspace because you are the owner"}, status=status.HTTP_400_BAD_REQUEST)
    
class WorkspaceLabelListView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerWorkspacePermission]

    def post(self, request, workspace_id):
        workspace = Workspaces.objects.get(id=workspace_id)
        WorkspaceLabels.objects.create(
                workspace=workspace,
                name=request.data['name'],
                color=request.data['color']
        )
        return Response({"message": "Label created successfully"}, status=status.HTTP_201_CREATED)

class WorkspaceLabelDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerWorkspacePermission]

    def put(self, request, workspace_id, label_id):
        label = WorkspaceLabels.objects.get(id=label_id)
        print(label)
        print(request.data)
        serialier = WorkspaceLabelSerializer(data=request.data, partial=True, instance=label)
        if serialier.is_valid():
            serialier.save()
            return Response({"message": "Label updated successfully"}, status=status.HTTP_200_OK)
        return Response(serialier.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, workspace_id, label_id):
        label = WorkspaceLabels.objects.get(id=label_id)
        label.delete()
        return Response({"message": "Label deleted successfully"}, status=status.HTTP_200_OK)


class WorkspaceRequestListView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerWorkspacePermission]

    # get all requests pending of a workspace
    def get(self, request, workspace_id):
        requests = Request.objects.filter(workspace_id=workspace_id, status='pending')
        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
