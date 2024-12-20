from django.urls import path
from . import views

urlpatterns = [
    path('requests/', views.RequestListView.as_view(), name='request_list'),
    path('requests/<str:request_id>/', views.RequestDetailView.as_view(), name='request_detail'),
]