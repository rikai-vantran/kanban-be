from django.db import models
from api.workspaces.models import Workspaces
from api.profiles.models import Profile
import uuid

class Columns(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(Workspaces, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    card_orders = models.JSONField(default=list)
    def __str__(self):
        return self.name

class Cards(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    column = models.ForeignKey(Columns, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateField(blank=True, null=True)
    assigns = models.ManyToManyField(Profile, related_name='assigns')

    def __str__(self):
        return self.title

task_status = [
    ('todo', 'To Do'),
    ('progress', 'In Progress'),
    ('done', 'Done'),
]
class Tasks(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
    status = models.CharField(max_length=24, default='todo')

    def __str__(self):
        return self.title