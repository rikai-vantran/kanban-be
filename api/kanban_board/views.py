from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from api.kanban_board.serialize import ColumnSerializer, CardSerializer, TaskSerializer
from rest_framework.response import Response
from rest_framework import status
from api.kanban_board.models import Columns, Cards, Tasks
from api.workspaces.models import Workspaces

class ColumnsListView(APIView):
    permission_classes = [IsAuthenticated]

    def check_owner(self, workspace_id, user):
        workspace = Workspaces.objects.get(id=workspace_id)
        return workspace.owner == user

    @swagger_auto_schema(request_body=ColumnSerializer)
    def post(self, request):
        if not self.check_owner(request.data['workspace_id'], request.user):
            return Response({
                "error": "You are not the owner of this workspace"
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = ColumnSerializer(data=request.data)
        if serializer.is_valid():
            Columns.objects.create(
                workspace_id=Workspaces.objects.get(id=request.data['workspace_id']),
                name=serializer.validated_data['name'],
                card_orders='[]'
            )
            return Response({
                "message": "Column created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        id = request.query_params.get('workspace_id')
        if Workspaces.objects.filter(id=id).count() == 0:
            return Response({
                "error": "Workspace not found"
            }, status=status.HTTP_404_NOT_FOUND)

        members = Workspaces.objects.get(id=id).members.all()
        if not request.user.profile in members:
            return Response({
                "error": "You are not a member of this workspace"
            }, status=status.HTTP_403_FORBIDDEN)

        columns = ColumnSerializer(Columns.objects.all().filter(workspace_id

class ColumnDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, column_id):
        column = Columns.objects.get(id=column_id)
        serializer = ColumnSerializer(column, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Column updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, column_id):

        if Columns.objects.filter(id=column_id).count() == 0:
            return Response({
                "error": "Column not found"
            }, status=status.HTTP_404_NOT_FOUND)
        if Columns.objects.get(id=column_id).workspace_id.members.filter(user=request.user).count() == 0:
            return Response({
                "error": "You are not a member of this workspace"
            }, status=status.HTTP_403_FORBIDDEN)
        Columns.objects.get(id=column_id).delete()
        return Response({
            "message": "Column deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


class CardsListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CardSerializer)

    def post(self, request):
        serializer = CardSerializer(data = request.data)
        if serializer.is_valid():
            Cards.objects.create(
                column_id = Columns.objects.get(id=request.data['column_id']),
                content = serializer.validated_data['content'],
                due_date = serializer.validated_data['due_date'],
                assign = serializer.validated_data['assign']
            )
            return Response({
                "message": "Card created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        id = request.query_params.get('column_id')
        if(Columns.objects.filter(id=id).count() == 0):
            return Response({
                "error": "Column not found"
            }, status=status.HTTP_404_NOT_FOUND)
        members = Columns.objects.get(id=id).workspace_id.members.filter(user=request.user)
        if members.count() == 0:
            return Response({
                "error": "You are not a member of this workspace"
            }, status=status.HTTP_403_FORBIDDEN)


        cards = CardSerializer(Cards.objects.all().filter(column_id=id), many=True)
        return Response({
            "data": cards.data
        }, status=status.HTTP_200_OK)

class CardsDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, card_id):
        card = Cards.objects.get(id=card_id)
        serializer = CardSerializer(card, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Card updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, card_id):
        if Cards.objects.filter(id=card_id).count() == 0:
            return Response({
                "error": "Card not found"
            }, status=status.HTTP_404_NOT_FOUND)
        member = Cards.objects.get(id=card_id).column_id.workspace_id.members.filter(user=request.user)
        if member.count() == 0:
            return Response({
                "error": "You are not a member of this workspace"
            }, status=status.HTTP_403_FORBIDDEN)
        Cards.objects.get(id=card_id).delete()
        return Response({
            "message": "Card deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


