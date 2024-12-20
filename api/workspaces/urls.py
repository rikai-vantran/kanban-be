from django.urls import path
from . import views

urlpatterns = [
    path('', views.WorkspaceListView.as_view(), name='workspace'),
    path('<str:workspace_id>/owner/', views.WorkspaceOwnerDetailView.as_view(), name='workspace-owner'),
    path('<str:workspace_id>/', views.WorkspaceDetailView.as_view(), name='workspace-detail'),
    path('<str:workspace_id>/members/', views.WorkspaceMemberListView.as_view(), name='workspace-members'),
    path('<str:workspace_id>/requests/', views.WorkspaceRequestListView.as_view(), name='workspace-requests'),
]