from django.urls import path
from . import views


urlpatterns = [
    path('kanban_column/', views.ColumnsListView.as_view(), name='columns'),
    path('<int:column_id>/', views.ColumnDetailView.as_view(), name='column-detail'),
    path('kanban_card/', views.CardsListView.as_view(), name='cards'),
    path('kanban_card/<int:card_id>/', views.CardsDetailView.as_view(), name='card-detail'),
]