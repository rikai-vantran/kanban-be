from django.urls import path
from . import views

urlpatterns = [
    path('columns/', views.ColumnsListView.as_view(), name='columns'),
    # path('kanban_column/update-all-card/', views.UpdateAllCard.as_view(), name='update-all-card'),
    # path('update-card-order-in-column/', views.UpdateCardOrderInColumn.as_view(), name='update-card-order-in-column'),
    path('columns/update_card_order/', views.UpdateCardOrder.as_view(), name='update_card_order'),
    path('columns/update_card_to_new_column/', views.UpdateCardToNewColumn.as_view(), name='update_card_to_new_column'),
    path('columns/<int:column_id>/', views.ColumnDetailView.as_view(), name='column-detail'),
    path('kanban_card/', views.CardsListView.as_view(), name='cards'),
    path('kanban_card/<int:card_id>/', views.CardsDetailView.as_view(), name='card-detail'),
    path('tasks/', views.TasksListView.as_view(), name='tasks'),
    path('tasks/<int:task_id>/', views.TasksDetailView.as_view(), name='task-detail'),
]