from django.db import models
from api.workspaces.models import Workspaces
from api.profiles.models import Profile

class Columns(models.Model):
    workspace_id = models.ForeignKey(Workspaces, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    card_orders = models.JSONField(default=list, null=True, blank=True)
    def __str__(self):
        return self.name

class Cards(models.Model):
    column_id = models.ForeignKey(Columns, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
    due_date = models.DateField(null=True, blank=True)
    assign = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


task_status = [
    ('in progress', 'In Progress'),
    ('done', 'Done'),
]
class Tasks(models.Model):
    content = models.CharField(max_length=256)
    status = models.CharField(max_length=256, choices=task_status)
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)


    def __str__(self):
        return self.title