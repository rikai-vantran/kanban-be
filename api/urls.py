from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('workspaces/', include('api.workspaces.urls')),
    path('workspaces/<int:workspace_id>/', include('api.kanban_board.urls')),
]