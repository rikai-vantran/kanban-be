# chat/routing.py
from django.urls import re_path
from api.workspaces.consumers import WorkspaceConsumer
from api.profiles.consumers import UserConsumer

websocket_urlpatterns = [
    re_path(r"ws/user/(?P<uid>\w+)/$", UserConsumer.as_asgi()),
    re_path(r"ws/workspace/(?P<workspace_id>\w+)/$", WorkspaceConsumer.as_asgi()),
]