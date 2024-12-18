from django.urls import path
from . import views


urlpatterns = [
    path('kanban_column/', views.ColumnsListView.as_view(), name='columns'),
    # path('kanban_column/update-all-card/', views.UpdateAllCard.as_view(), name='update-all-card'),
    # path('update-card-order-in-column/', views.UpdateCardOrderInColumn.as_view(), name='update-card-order-in-column'),
    path('update-card-order/', views.UpdateCardOrder.as_view(), name='update-card-order'),
    path('update-card-to-new-column/', views.UpdateCardToNewColumn.as_view(), name='update-card-to-new-column'),
    path('<int:column_id>/', views.ColumnDetailView.as_view(), name='column-detail'),
    path('kanban_card/', views.CardsListView.as_view(), name='cards'),
    path('kanban_card/<int:card_id>/', views.CardsDetailView.as_view(), name='card-detail'),
]