from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Request
from .serializers import RequestSerializer, AcceptRejectRequestSerializer
from drf_yasg.utils import swagger_auto_schema
from api.models import WorkspaceMembers
from api.profiles.serializers import ProfileWorkspaceSerializer
from api.notifications.permissions import IsUserReceiverPermission
from api.models import Profile


class RequestListView(APIView):
    permission_classes = [IsAuthenticated]

    # Get all requests of the user
    def get(self, request):
        try:
            requests = Request.objects.filter(user_receiver=request.user.profile)
            serializer = RequestSerializer(requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Request.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # Send a request to a user
    @swagger_auto_schema(request_body=RequestSerializer)
    def post(self, request):
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            # check user_receiver is not the same as user_sender
            if serializer.validated_data['user_receiver'] == request.user.profile:
                return Response({"error": "You cannot send a request to yourself"}, status=status.HTTP_400_BAD_REQUEST)
            # check sender_user is owner of workspace
            if serializer.validated_data['workspace'].members.filter(user=request.user, workspacemembers__role='owner').exists() == False:
                return Response({"error": "You must be the owner of the workspace to send a request"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(user_sender=request.user.profile)
            return Response({
                "message": "Request sent successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestDetailView(APIView):
    permission_classes = [IsAuthenticated, IsUserReceiverPermission]

    @swagger_auto_schema(request_body=AcceptRejectRequestSerializer)
    def put(self, request, request_id):
        try:
            requestNotification = Request.objects.get(id=request_id)
            serializer = AcceptRejectRequestSerializer(
                requestNotification, data=request.data, partial=True)
            if serializer.is_valid():
                # update request status
                Request.objects.filter(id=request_id).update(
                    status=serializer.validated_data['status'])
                # add user to workspace with role member if request is accepted
                if serializer.validated_data['status'] == 'accepted':
                    workspace = requestNotification.workspace
                    member = requestNotification.user_receiver
                    # check user is already a member of the workspace
                    if workspace.members.filter(user_id=member.user_id).exists():
                        return Response({"error": "User is already a member of the workspace"}, status=status.HTTP_400_BAD_REQUEST)
                    WorkspaceMembers.objects.create(
                        workspace=workspace, member=member, role='member')
                    # Add workspace to the user's workspace_member_orders
                    profile = Profile.objects.get(user=member.user)
                    profileSerializer = ProfileWorkspaceSerializer(
                        profile,
                        data={
                            'workspace_member_orders': list(profile.workspace_member_orders) + [workspace.id]
                        },
                        partial=True
                    )
                    if profileSerializer.is_valid():
                        profileSerializer.save()
                return Response({
                    "meseage": "Request updated successfully"
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Request.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, request_id):
        try:
            request = Request.objects.get(id=request_id)
            request.delete()
            return Response(
                {"message": "Request deleted successfully"},
                status=status.HTTP_200_OK
            )
        except Request.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)