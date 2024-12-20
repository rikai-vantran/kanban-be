from django.db import models
from api.profiles.models import Profile
from api.workspaces.models import Workspaces
import uuid

class Notifications(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_receiver = models.ForeignKey(Profile, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspaces, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    
request_status = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected')
]
class Request(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_sender')
    user_receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_receiver')
    workspace = models.ForeignKey(Workspaces, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=request_status, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user_sender', 'user_receiver', 'workspace']
        ordering = ['-created_at']