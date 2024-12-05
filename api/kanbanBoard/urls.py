from django.urls import path
from . import views


urlpatterns = [
    path('columns/', views.ColumnsListView.as_view(), name='columns'),
    path('columns/<int:column_id>/', views.ColumnDetailView.as_view(), name='column-detail'),
    path('cards/', views.CardsListView.as_view(), name='cards'),
    path('cards/<int:card_id>/', views.CardsDetailView.as_view(), name='card-detail'),
]