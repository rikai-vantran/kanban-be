from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfileListView.as_view(), name='profile_list'),
    path('<int:profile_id>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    
    path('me/', views.ProfileMeDetailView.as_view(), name='profile_me'),
    path('avatars/', views.UserAvatarListView.as_view(), name='user_avatar_list'),
    path('workspace-owner-orders/', views.ProfileWorkspaceOwnerOrdersView.as_view(), name='profile_workspace_owner_orders'),
]