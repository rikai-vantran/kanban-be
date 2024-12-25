from django.db import models
from api.profiles.models import Profile
import uuid

class Workspaces(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=128)
    icon_unified = models.CharField(max_length=64)
    column_orders = models.JSONField(default=list)
    create_at = models.DateTimeField(auto_now_add=True)

    members = models.ManyToManyField(Profile, through="WorkSpaceMembers")

    def __str__(self):
        return self.name

class WorkspaceMembers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Profile, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspaces, on_delete=models.CASCADE)

    role = models.CharField(choices=(
        ('owner', 'Owner'),
        ('member', 'Member'),
    ), max_length=6)

    def __str__(self):
        return f"{self.member.user.email} - {self.workspace.name}"

class WorkspaceLogs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace= models.ForeignKey(Workspaces, on_delete=models.CASCADE)
    log = models.TextField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)