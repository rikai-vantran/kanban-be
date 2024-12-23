from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from api.kanbanBoard.serialize import ColumnSerializer, CardSerializer
from rest_framework.response import Response
from rest_framework import status
from api.kanbanBoard.models import Columns
from api.workspaces.permissions import IsOwnerOrMemberWorkspacePermission
from api.workspaces.models import Workspaces
from rest_framework.parsers import MultiPartParser, FormParser


class ColumnsListView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrMemberWorkspacePermission]

    # create a new column
    @swagger_auto_schema(operation_summary="Create a new column", request_body=ColumnSerializer)
    def post(self, request, workspace_id):
        request.data['workspace'] = workspace_id
        serializer = ColumnSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # update column_orders in workspace
            workspace = Workspaces.objects.get(id=workspace_id)
            workspace.column_orders.append(serializer.data['id'])
            workspace.save()
            return Response({
                "message": "Column created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # get all columns in a workspace
    def get(self, request, workspace_id):
        serializer = ColumnSerializer(Columns.objects.all().filter(
            workspace_id=workspace_id), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ColumnDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrMemberWorkspacePermission]

    # update a column by id
    @swagger_auto_schema(operation_summary="Update a column", request_body=ColumnSerializer)
    def put(self, request, column_id, workspace_id):
        request.data['workspace'] = workspace_id
        # check if column exists
        if Columns.objects.filter(id=column_id, workspace_id=workspace_id).count() == 0:
            return Response({
                "error": "Column not found"
            }, status=status.HTTP_404_NOT_FOUND)

        column = Columns.objects.get(id=column_id)
        serializer = ColumnSerializer(column, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Column updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete a column by id
    def delete(self, request, column_id, workspace_id):
        # check if column exists
        if Columns.objects.filter(id=column_id, workspace_id=workspace_id).count() == 0:
            return Response({
                "error": "Column not found"
            }, status=status.HTTP_404_NOT_FOUND)

        column = Columns.objects.get(id=column_id)
        column.delete()
        # update column_orders in workspace
        workspace = Workspaces.objects.get(id=workspace_id)
        workspace.column_orders.remove(column_id)
        workspace.save()
        return Response({
            "message": "Column deleted successfully"
        }, status=status.HTTP_200_OK)


class CardListView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrMemberWorkspacePermission]

    # create a new card
    @swagger_auto_schema(operation_summary="Create a new card", request_body=CardSerializer)
    def post(self, request, workspace_id, column_id):
        # check if column exists
        if Columns.objects.filter(id=column_id, workspace_id=workspace_id).count() == 0:
            return Response({
                "error": "Column not found"
            }, status=status.HTTP_404_NOT_FOUND)
        request.data['column'] = column_id
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # update card_orders in column
            column = Columns.objects.get(id=column_id)
            column.card_orders.append(serializer.data['id'])
            column.save()
            return Response({
                "message": "Card created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # get all cards in a column
    def get(self, request, workspace_id, column_id):
        # check if column exists
        if Columns.objects.filter(id=column_id, workspace_id=workspace_id).count() == 0:
            return Response({
                "error": "Column not found"
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = CardSerializer(Columns.objects.get(
            id=column_id).cards_set.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CardDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrMemberWorkspacePermission]
    # update a card by id
    @swagger_auto_schema(operation_summary="Update a card", request_body=CardSerializer)
    def put(self, request, card_id, workspace_id, column_id):
        # check if column exists
        if Columns.objects.filter(id=column_id, workspace_id=workspace_id).count() == 0:
            return Response({
                "error": "Column not found"
            }, status=status.HTTP_404_NOT_FOUND)
        card = Columns.objects.get(id=column_id).cards_set.get(id=card_id)
        # check if card exists
        if (card is None):
            return Response({
                "error": "Card not found"
            }, status=status.HTTP_404_NOT
        )
        if not request.data.get('column'):
            request.data['column'] = column_id
        serializer = CardSerializer(card, data=request.data, partial=True, context={'workspace_id': workspace_id})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Card updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete a card by id
    def delete(self, request, card_id, workspace_id, column_id):
        # check if column exists
        if Columns.objects.filter(id=column_id, workspace_id=workspace_id).count() == 0:
            return Response({
                "error": "Column not found"
            }, status=status.HTTP_404_NOT_FOUND)
        # check if card exists
        if Columns.objects.get(id=column_id).cards_set.filter(id=card_id).count() == 0:
            return Response({
                "error": "Card not found"
            }, status=status.HTTP_404_NOT_FOUND)

        card = Columns.objects.get(id=column_id).cards_set.get(id=card_id)
        card.delete()
        # update card_orders in column
        column = Columns.objects.get(id=column_id)
        column.card_orders.remove(card_id)
        column.save()
        return Response({
            "message": "Card deleted successfully"
        }, status=status.HTTP_200_OK)


class CardWorkspaceListView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrMemberWorkspacePermission]

    # get all cards in a workspace
    def get(self, request, workspace_id):
        columns = Columns.objects.all().filter(workspace_id=workspace_id)
        cards = []
        for column in columns:
            for card in column.cards_set.all():
                cards.append(card)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class TasksListView(APIView):
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(request_body=TaskSerializer)
#     def post(self, request):
#         if Cards.objects.filter(id=request.data['card']).count() == 0:
#             return Response({
#                 "error": "Card not found"
#             }, status=status.HTTP_404_NOT_FOUND)

#         member = Cards.objects.get(id=request.data['card']).column_id.workspace_id.members.filter(user=request.user)
#         if member.count() == 0:
#             return Response({
#                 "error": "You are not a member of this workspace"
#             }, status=status.HTTP_403_FORBIDDEN)
#         serializer = TaskSerializer(data = request.data)
#         if serializer.is_valid():
#             Tasks.objects.create(
#                 card = serializer.validated_data['card'],
#                 content = serializer.validated_data['content'],
#                 status = serializer.validated_data['status']
#             )
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request):
#         id = request.query_params.get('card_id')
#         if Cards.objects.filter(id=id).count() == 0:
#             return Response({
#                 "error": "Card not found"
#             }, status=status.HTTP_404_NOT_FOUND)
#         member = Cards.objects.get(id=id).column_id.workspace_id.members.filter(user=request.user)
#         if member.count() == 0:
#             return Response({
#                 "error": "You are not a member of this workspace"
#             }, status=status.HTTP_403_FORBIDDEN)
#         tasks = Tasks.objects.filter(card_id=id)
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class TasksDetailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def put(self, request, task_id):
#         if Tasks.objects.filter(id=task_id).count() == 0:
#             return Response({
#                 "error": "Task not found"
#             }, status=status.HTTP_404_NOT_FOUND)
#         member = Tasks.objects.get(id=task_id).card.column_id.workspace_id.members.filter(user=request.user)
#         if member.count() == 0:
#             return Response({
#                 "error": "You are not a member of this workspace"
#             }, status=status.HTTP_403_FORBIDDEN)
#         task = Tasks.objects.get(id=task_id)
#         serializer = TaskSerializer(task, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "message": "Task updated successfully",
#                 "data": serializer.data
#             }, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, task_id):
#         if Tasks.objects.filter(id=task_id).count() == 0:
#             return Response({
#                 "error": "Task not found"
#             }, status=status.HTTP_404_NOT_FOUND)
#         member = Tasks.objects.get(id=task_id).card.column_id.workspace_id.members.filter(user=request.user)
#         if member.count() == 0:
#             return Response({
#                 "error": "You are not a member of this workspace"
#             }, status=status.HTTP_403_FORBIDDEN)
#         Tasks.objects.get(id=task_id).delete()
#         return Response({
#             "message": "Task deleted successfully"
#         }, status=status.HTTP_204_NO_CONTENT)