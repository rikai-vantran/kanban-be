from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from api.kanbanBoard.serialize import ColumnSerializer, CardSerializer, TaskSerializer
from rest_framework.response import Response
from rest_framework import status
from api.kanbanBoard.models import Columns, Tasks
from api.workspaces.permissions import IsOwnerOrMemberWorkspacePermission
from api.workspaces.models import Workspaces
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from api.kanbanBoard.models import Cards
from utils.cloudinary_upload_services import upload_file


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
        serializer = CardSerializer(data=request.data, context={
                                    'workspace_id': workspace_id})
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

    # get card detail by id
    def get(self, request, card_id, workspace_id, column_id):
        # check if card exists
        if Cards.objects.filter(id=card_id).count() == 0:
            return Response({
                "error": "Card not found"
            }, status=status.HTTP_404_NOT_FOUND)

        card = Cards.objects.get(id=card_id)
        serializer = CardSerializer(card)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # update a card by id
    @swagger_auto_schema(operation_summary="Update a card", request_body=CardSerializer)
    def put(self, request, card_id, workspace_id, column_id):

        # validate request -----------------------------------
        # check if column exists
        if Columns.objects.filter(id=column_id, workspace_id=workspace_id).count() == 0:
            return Response({
                "error": "Column not found"
            }, status=status.HTTP_404_NOT_FOUND)
        card = Cards.objects.get(id=card_id)
        # --------------------------------------------------------

        clone_request = request.data.copy()
        if not request.data.get('column'):
            clone_request['column'] = column_id
        serializer = CardSerializer(card, data=clone_request, partial=True, context={
                                    'workspace_id': workspace_id})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Card updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(
            # serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)

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


class MoveCardSameColumnView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrMemberWorkspacePermission]

    def post(self, request, workspace_id):
        # check if column exists in workspace
        column_id = request.data.get('column_id')
        if Columns.objects.filter(id=column_id, workspace_id=workspace_id).count() == 0:
            return Response({
                "error": "Column not found"
            }, status=status.HTTP_404_NOT_FOUND)

        card_orders = request.data.get('card_orders')
        serializer = ColumnSerializer(
            Columns.objects.get(id=column_id),
            data={
                "card_orders": card_orders
            },
            partial=True
        )
        if (serializer.is_valid()):
            serializer.save()
            return Response({
                "message": "Card moved successfully"
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MoveCardCrossColumnView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrMemberWorkspacePermission]

    def post(self, request, workspace_id):
        try:
            pre_column_id = request.data.get('pre_column_id')
            next_column_id = request.data.get('next_column_id')
            pre_card_orders = request.data.get('pre_card_orders')
            next_card_orders = request.data.get('next_card_orders')
            card_id = request.data.get('card_id')

            # check if card exists in workspace
            if Columns.objects.filter(id=pre_column_id, workspace_id=workspace_id).count() == 0:
                return Response({
                    "error": "Column not found"
                }, status=status.HTTP_404_NOT_FOUND)

            card = Cards.objects.get(id=card_id)
            # change column of card
            card.column_id = next_column_id
            card.save()

            # update card_orders in pre_column
            pre_serializer = ColumnSerializer(
                Columns.objects.get(id=pre_column_id),
                data={
                    "card_orders": pre_card_orders
                },
                partial=True
            )
            if (pre_serializer.is_valid()):
                pre_serializer.save()

            # update card_orders in next_column
            next_serializer = ColumnSerializer(
                Columns.objects.get(id=next_column_id),
                data={
                    "card_orders": next_card_orders
                },
                partial=True
            )
            if (next_serializer.is_valid()):
                next_serializer.save()

            return Response({
                "message": "Card moved successfully"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class CardImageUploadView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrMemberWorkspacePermission]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, workspace_id, column_id, card_id):
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
        card = Cards.objects.get(id=card_id)
        if 'file' not in request.data:
            return Response({
                "error": "Image not found"
            }, status=status.HTTP_400_BAD_REQUEST)
        image = request.data['file']
        card.image = upload_file(image, public_id=f"{card_id}")
        card.save()
        return Response({
            "message": "Image uploaded successfully",
            "data": card.image
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


class TaskListView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrMemberWorkspacePermission]

    @swagger_auto_schema(request_body=TaskSerializer)
    # create task for a card
    def post(self, request, column_id, card_id, workspace_id):
        # check card exists
        if Cards.objects.filter(id=card_id).filter(column_id=column_id).count() == 0:
            return Response({
                "error": "Card not found"
            }, status=status.HTTP_404_NOT_FOUND)

        card = Cards.objects.get(id=card_id)
        serializer = TaskSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save(card=card)
            return Response({
                "message": "Task created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "error": serializer.error_messages,
        }, status=status.HTTP_400_BAD_REQUEST)

    # get all tasks for a card
    def get(self, request, column_id, card_id, workspace_id):
        # check card exists
        if Cards.objects.filter(id=card_id).filter(column_id=column_id).count() == 0:
            return Response({
                "error": "Card not found"
            }, status=status.HTTP_404_NOT_FOUND)

        card = Cards.objects.get(id=card_id)
        serializer = TaskSerializer(card.tasks_set.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    # edit task by id
    def put(self, request, column_id, card_id, workspace_id, task_id):
        # check task exists
        if Tasks.objects.filter(id=task_id).count() == 0:
            return Response({
                "error": "Task not found"
            }, status=status.HTTP_404_NOT_FOUND)

        task = Tasks.objects.get(id=task_id)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Task updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete task by id
    def delete(self, request, column_id, card_id, workspace_id, task_id):
        # check task exists
        if Tasks.objects.filter(id=task_id).count() == 0:
            return Response({
                "error": "Task not found"
            }, status=status.HTTP_404_NOT_FOUND)

        task = Tasks.objects.get(id=task_id)
        task.delete()
        return Response({
            "message": "Task deleted successfully"
        }, status=status.HTTP_200_OK)
