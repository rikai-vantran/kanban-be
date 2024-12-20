from django.urls import path
from django.urls import include
from django.urls import re_path
from api.profiles.consumers import UserConsumer

websocket_urlpatterns = [
    # re_path(r"ws/user/(?P<uid>\w+)/$", UserConsumer.as_asgi()),
    re_path(r"ws/user/", UserConsumer.as_asgi()),
]

urlpatterns = [
    path('workspaces/', include('api.workspaces.urls')),
    path('workspaces/<str:workspace_id>/', include('api.kanbanBoard.urls')),
    path('profiles/', include('api.profiles.urls')),
    path('notifications/', include('api.notifications.urls')),
]