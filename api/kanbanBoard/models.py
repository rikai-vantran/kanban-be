from django.db import models
from api.workspaces.models import Workspaces
from api.profiles.models import Profile

class Columns(models.Model):
    workspace = models.ForeignKey(Workspaces, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    card_orders = models.JSONField(default=list)
    def __str__(self):
        return self.name

class Cards(models.Model):
    column = models.ForeignKey(Columns, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
    due_date = models.DateField(null=True, blank=True)
    assign = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


task_status = [
    ('todo', 'To Do'),
    ('progress', 'In Progress'),
    ('done', 'Done'),
]
class Tasks(models.Model):
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
    status = models.CharField(max_length=24, default='todo')

    def __str__(self):
        return self.title