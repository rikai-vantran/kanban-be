from django.urls import path
from . import views

urlpatterns = [
    path('', views.WorkspaceListView.as_view(), name='workspace'),
    path('<int:workspace_id>/', views.WorkspaceDetailView.as_view(), name='workspace-detail'),
    path('column_order/<int:workspace_id>/', views.ColumnUpdateOrder.as_view(), name='column-order'),
]