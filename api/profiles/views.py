from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserAvatarSerializer, ProfileWorkspaceSerializer, ProfileInfoSerializer, ProfileSerializer
from api.models import Profile, UserAvatar
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema

# Get Profile Me
class ProfileMeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    # Get Profile Me
    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # Update Profile Me
    @swagger_auto_schema(request_body=ProfileInfoSerializer)
    def put(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileInfoSerializer(
                profile,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Profile updated successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# Get Profile Detail by ID
class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, profile_id):
        try:
            profile = Profile.objects.get(user__id=profile_id)
            serializer = ProfileInfoSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# Get Profile, filter by email exact
class ProfileListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.query_params.get('email')
        if email:
            profiles = Profile.objects.filter(user__email=email)
        else:
            profiles = Profile.objects.all()
        serializer = ProfileInfoSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Edit Workspace Owner Orders
class ProfileWorkspaceOwnerOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileWorkspaceSerializer(
                profile,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# Get All Avatars Default


class UserAvatarListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            user_avatars = UserAvatar.objects.all()
            serializer = UserAvatarSerializer(user_avatars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserAvatar.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
