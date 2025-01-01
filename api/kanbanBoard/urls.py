from django.urls import path
from . import views


urlpatterns = [
    path('columns/', views.ColumnsListView.as_view(), name='columns'),
    path('columns/<str:column_id>/', views.ColumnDetailView.as_view(), name='column-detail'),
    path('columns/<str:column_id>/cards/', views.CardListView.as_view(), name='cards'),
    path('columns/<str:column_id>/cards/<str:card_id>/', views.CardDetailView.as_view(), name='card-detail'),
    path('columns/<str:column_id>/cards/<str:card_id>/image/', views.CardImageUploadView.as_view(), name='upload-image'),
    
    path('move-card-same-column/', views.MoveCardSameColumnView.as_view(), name='move-card-same-column'),
    path('move-card-cross-column/', views.MoveCardCrossColumnView.as_view(), name='move-card-cross-column'),
    path('cards/', views.CardWorkspaceListView.as_view(), name='cards-workspace'),

    path('columns/<str:column_id>/cards/<str:card_id>/tasks/', views.TaskListView.as_view(), name='tasks'),
    path('columns/<str:column_id>/cards/<str:card_id>/tasks/<str:task_id>/', views.TaskDetailView.as_view(), name='task-detail'),
]