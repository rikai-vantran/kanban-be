from django.db import models
from api.workspaces.models import Workspaces
from api.profiles.models import Profile
import uuid
from api.models import WorkspaceLabels

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
    short_description = models.TextField(null=True, blank=True)
    description = models.JSONField(default=list)
    image = models.URLField(null=True, blank=True)
    due_date = models.DateTimeField(blank=True, null=True)
    labels = models.ManyToManyField(WorkspaceLabels, related_name='cards', blank=True)
    assigns = models.ManyToManyField(Profile, related_name='assigns', blank=True)

    def __str__(self):
        return self.name
class Tasks(models.Model):
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title