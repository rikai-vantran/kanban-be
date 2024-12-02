from django.db import models
from api.profiles.models import Profile
from api.workspaces.models import Workspaces

class Notifications(models.Model):
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
    user_receiver = models.ForeignKey(Profile, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspaces, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=request_status, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

