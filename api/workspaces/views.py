from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import WorkspaceSerializer, GetAllWorkSpaceSerializer
from drf_yasg.utils import swagger_auto_schema
from api.models import Workspaces, Profile, WorkspaceMembers
from api.profiles.serializers import ProfileSerializer

class WorkspaceListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=WorkspaceSerializer)
    def post(self, request):
        serializer = WorkspaceSerializer(data = request.data)
        if serializer.is_valid():
            workspace = Workspaces.objects.create(
                name = serializer.validated_data['name'],
                icon_unified = serializer.validated_data['icon_unified'],
                column_orders = '[]'
            )
            profile = Profile.objects.get(user=request.user)
            workspace.members.add(profile, through_defaults={"role": 'owner'})
            profileSerializer = ProfileSerializer(
                profile,
                data = {
                    'workspace_owner_orders': list(Profile.objects.get(user=request.user).workspace_owner_orders) + [workspace.id]
                },
                partial=True
            )
            if not profileSerializer.is_valid():
                return Response(profileSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            profileSerializer.save()

            return Response({
                "message": "Workspace created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        role = request.query_params.get('role')
        print(role)
        profile = Profile.objects.get(user=request.user)
        workspaceMembers = WorkspaceMembers.objects.filter(member=profile)

        if role == 'member':
            workspaceMembers = workspaceMembers.filter(role='member')
        elif role == 'owner':
            workspaceMembers = workspaceMembers.filter(role='owner')
        elif role:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = GetAllWorkSpaceSerializer(workspaceMembers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class WorkspaceDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, workspace_id):
        # Check if the user is the owner of the workspace
        workspaceMembers = WorkspaceMembers.objects.filter(workspace=workspace_id)
        if not workspaceMembers.filter(role='owner', member__user=request.user).exists():
            return Response({"error": "You can't delete this workspace"}, status=status.HTTP_403_FORBIDDEN)
        
        Workspaces.objects.get(id=workspace_id).delete()
        profile = Profile.objects.get(user=request.user)
        profile.workspaces_set.remove(workspace_id)
        profile.workspace_owner_orders.remove(workspace_id)
        profile.save()
        return Response({"message": "Workspace deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    # def get(self, request, workspace_id):
    #     workspace = Workspaces.objects.get(id=workspace_id)
    #     serializer = AddWorkspaceSerializer(workspace)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, workspace_id):
        workspace = Workspaces.objects.get(id=workspace_id)
        serializer = WorkspaceSerializer(workspace, data=request.data)
        if serializer.is_valid():
            workspace.name = serializer.validated_data['name']
            workspace.icon_unified = serializer.validated_data['icon_unified']
            workspace.save()
            return Response({
                "message": "Workspace updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)