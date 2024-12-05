# chat/routing.py
from django.urls import re_path
from api.profiles.consumers import UserConsumer

websocket_urlpatterns = [
    # real-time user profile updates (workspace_member_orders)
    # ws://localhost:8000/ws/user/<uid>/
    # {"workspace_members": [], "workspace_member_orders": []}
    re_path(r"ws/user/(?P<uid>\w+)/$", UserConsumer.as_asgi()),
]