from django.urls import path
from . import views


urlpatterns = [
    path('columns/', views.ColumnsListView.as_view(), name='columns'),
    path('columns/<str:column_id>/', views.ColumnDetailView.as_view(), name='column-detail'),
    path('columns/<str:column_id>/cards/', views.CardListView.as_view(), name='cards'),
    path('columns/<str:column_id>/cards/<str:card_id>/', views.CardDetailView.as_view(), name='card-detail'),

    path('cards/', views.CardWorkspaceListView.as_view(), name='cards-workspace'),
]