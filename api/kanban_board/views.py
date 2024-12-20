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

    @swagger_auto_schema(request_body=ColumnSerializer)
    def post(self, request):
        if Workspaces.objects.filter(id=request.data['workspace_id']).count() == 0:
            return Response({
                "error": "Workspace not found"
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = ColumnSerializer(data=request.data)
        if serializer.is_valid():
            Columns.objects.create(
                workspace_id=Workspaces.objects.get(id=request.data['workspace_id']),
                name=serializer.validated_data['name'],
                card_orders=[]
            )
            # add column to workspace order
            workspace = Workspaces.objects.get(id=request.data['workspace_id'])
            id_col = Columns.objects.last().id
            workspace.column_orders.append(id_col)
            workspace.save()
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
        columns = ColumnSerializer(Columns.objects.all().filter(workspace_id=id), many=True)
        return Response(columns.data, status=status.HTTP_200_OK)

class ColumnDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, column_id):
        if Columns.objects.filter(id=column_id).count() == 0:
            return Response({
                "error": "Column not found"
            }, status=status.HTTP_404_NOT_FOUND)
        if Columns.objects.get(id=column_id).workspace_id.members.filter(user=request.user).count() == 0:
            return Response({
                "error": "You are not a member of this workspace"
            }, status=status.HTTP_403_FORBIDDEN)
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
        workspace = Columns.objects.get(id=column_id).workspace_id
       #convert column_id to list
        # column_id = Columns.objects.get(id=column_id).id
        print(type(workspace.column_orders))
        print(type(column_id))
        workspace.column_orders.remove(column_id)
        workspace.save()
        Columns.objects.get(id=column_id).delete()
        ## delete column from workspace order
        return Response({
            "message": "Column deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)

class UpdateCardOrder(APIView):
    def put(self, request, *args, **kwargs):
        if Columns.objects.get(id=request.data['over_column_id']).workspace_id.members.filter(user=request.user).count() == 0:
            return Response({
                "error": "You are not a member of this workspace"
            }, status=status.HTTP_403_FORBIDDEN)
        over_column_id = request.data.get('over_column_id')
        active_card_id = (request.data.get('active_card_id'))
        card_orders = request.data.get('card_orders', [])
        #change Idcol of card to over column
        card = Cards.objects.get(id=active_card_id)
        card.column_id = Columns.objects.get(id=over_column_id)
        card.save()
        #get all column
        all_columns = Columns.objects.all()
        #delete card order in column
        for column in all_columns:
            idCardOrder = column.card_orders
            for id in idCardOrder:
                if id == active_card_id:
                    column.card_orders.remove(id)
                    column.save()
        over_colum = Columns.objects.get(id=over_column_id)
        over_colum.card_orders = card_orders
        over_colum.save()
        return Response({
            "message": "Card order updated successfully"
        }, status=status.HTTP_200_OK)

class UpdateCardToNewColumn(APIView):
    def put(self, request, *args, **kwargs):
        if Columns.objects.get(id=request.data['over_column_id']).workspace_id.members.filter(user=request.user).count() == 0:
            return Response({
                "error": "You are not a member of this workspace"
            }, status=status.HTTP_403_FORBIDDEN)

        over_column_id = request.data.get('over_column_id')
        active_card_id = (request.data.get('active_card_id'))
        #change Idcol of card to over column
        card = Cards.objects.get(id=active_card_id)
        card.column_id = Columns.objects.get(id=over_column_id)
        card.save()
        #get all column
        all_columns = Columns.objects.all()
        #delete card order in column
        for column in all_columns:
            idCardOrder = column.card_orders
            for id in idCardOrder:
                if id == active_card_id:
                    column.card_orders.remove(id)
                    column.save()
        over_colum = Columns.objects.get(id=over_column_id)
        over_colum.card_orders.append(active_card_id)
        over_colum.save()
        return Response({
            "message": "Card order updated successfully"
        }, status=status.HTTP_200_OK)

class CardsListView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=CardSerializer)
    def post(self, request):
        if Columns.objects.filter(id=request.data['column_id']).count() == 0:
            return Response({
                "error": "Column not found"
            }, status=status.HTTP_404_NOT_FOUND)
        members = Columns.objects.get(id=request.data['column_id']).workspace_id.members.filter(user=request.user)
        if members.count() == 0:
            return Response({
                "error": "You are not a member of this workspace"
            }, status=status.HTTP_403_FORBIDDEN)
        serializer = CardSerializer(data = request.data)
        if serializer.is_valid():
            Cards.objects.create(
                column_id = Columns.objects.get(id=request.data['column_id']),
                content = serializer.validated_data['content'],
                due_date = serializer.validated_data['due_date'],
                assign = serializer.validated_data['assign']
            )
            # add card to column order
            column = Columns.objects.get(id=request.data['column_id'])
            id_card = Cards.objects.last().id
            column.card_orders.append(id_card)
            column.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
        return Response(cards.data, status=status.HTTP_200_OK)

class CardsDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, card_id):
        if Cards.objects.filter(id=card_id).count() == 0:
            return Response({
                "error": "Card not found"
            }, status=status.HTTP_404_NOT_FOUND)
        member = Cards.objects.get(id=card_id).column_id.workspace_id.members.filter(user=request.user)
        if member.count() == 0:
            return Response({
                "error": "You are not a member of this workspace"
            }, status=status.HTTP_403_FORBIDDEN)
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
        column = Cards.objects.get(id=card_id).column_id
        column.card_orders.remove(card_id)
        column.save()
        Cards.objects.get(id=card_id).delete()
        return Response({
            "message": "Card deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)

class TasksListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=TaskSerializer)
    def post(self, request):
        if Cards.objects.filter(id=request.data['card']).count() == 0:
            return Response({
                "error": "Card not found"
            }, status=status.HTTP_404_NOT_FOUND)

        member = Cards.objects.get(id=request.data['card']).column_id.workspace_id.members.filter(user=request.user)
        if member.count() == 0:
            return Response({
                "error": "You are not a member of this workspace"
            }, status=status.HTTP_403_FORBIDDEN)
        serializer = TaskSerializer(data = request.data)
        if serializer.is_valid():
            Tasks.objects.create(
                card = serializer.validated_data['card'],
                content = serializer.validated_data['content'],
                status = serializer.validated_data['status']
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        id = request.query_params.get('card_id')
        if Cards.objects.filter(id=id).count() == 0:
            return Response({
                "error": "Card not found"
            }, status=status.HTTP_404_NOT_FOUND)
        member = Cards.objects.get(id=id).column_id.workspace_id.members.filter(user=request.user)
        if member.count() == 0:
            return Response({
                "error": "You are not a member of this workspace"
            }, status=status.HTTP_403_FORBIDDEN)
        tasks = Tasks.objects.filter(card_id=id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TasksDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, task_id):
        if Tasks.objects.filter(id=task_id).count() == 0:
            return Response({
                "error": "Task not found"
            }, status=status.HTTP_404_NOT_FOUND)
        member = Tasks.objects.get(id=task_id).card.column_id.workspace_id.members.filter(user=request.user)
        if member.count() == 0:
            return Response({
                "error": "You are not a member of this workspace"
            }, status=status.HTTP_403_FORBIDDEN)
        task = Tasks.objects.get(id=task_id)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Task updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id):
        if Tasks.objects.filter(id=task_id).count() == 0:
            return Response({
                "error": "Task not found"
            }, status=status.HTTP_404_NOT_FOUND)
        member = Tasks.objects.get(id=task_id).card.column_id.workspace_id.members.filter(user=request.user)
        if member.count() == 0:
            return Response({
                "error": "You are not a member of this workspace"
            }, status=status.HTTP_403_FORBIDDEN)
        Tasks.objects.get(id=task_id).delete()
        return Response({
            "message": "Task deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


