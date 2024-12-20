from django.db import models
from django.contrib.auth.models import User
from dirtyfields import DirtyFieldsMixin
import uuid

class Profile(models.Model, DirtyFieldsMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200)
    profile_pic = models.ForeignKey('UserAvatar', on_delete=models.SET_NULL, blank=True, null=True)
    workspace_owner_orders = models.JSONField(default=list, blank=True)
    workspace_member_orders = models.JSONField(default=list, blank=True)

class UserAvatar(models.Model):
    name = models.CharField(max_length=200)
    avatar = models.URLField()