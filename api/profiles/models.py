from django.db import models
from django.contrib.auth.models import User

avatar = [
    ('unicorn', 'https://firebasestorage.googleapis.com/v0/b/plantsnap-419307.appspot.com/o/kanban%2Fcool-.png?alt=media&token=b9cb3234-905c-4283-9f80-c496f994a843'),
    ('dragon', 'https://firebasestorage.googleapis.com/v0/b/plantsnap-419307.appspot.com/o/kanban%2Fdragon.png?alt=media&token=da996e1e-29d5-45d6-884b-47a848f4293e'),
    ('duck', 'https://firebasestorage.googleapis.com/v0/b/plantsnap-419307.appspot.com/o/kanban%2Fduck.png?alt=media&token=33c6a5dc-aa7b-470b-8d9f-5f38b6dfc233'),
    ('giraffe', 'https://firebasestorage.googleapis.com/v0/b/plantsnap-419307.appspot.com/o/kanban%2Fgiraffe.png?alt=media&token=ccfd663a-0903-48f8-bdb0-35f425667f90'),
    ('hippopotamus', 'https://firebasestorage.googleapis.com/v0/b/plantsnap-419307.appspot.com/o/kanban%2Fhippopotamus.png?alt=media&token=627a1a4b-4551-41f5-93e9-96c6467ca752'),
    ('lion', 'https://firebasestorage.googleapis.com/v0/b/plantsnap-419307.appspot.com/o/kanban%2Flion.png?alt=media&token=03011157-39a6-47a5-a03b-ab1be10263d3'),
    ('puffer-fish', 'https://firebasestorage.googleapis.com/v0/b/plantsnap-419307.appspot.com/o/kanban%2Fpuffer-fish.png?alt=media&token=5c003012-b4e0-459e-81ed-0930917f0545'),
    ('shark', 'https://firebasestorage.googleapis.com/v0/b/plantsnap-419307.appspot.com/o/kanban%2Fshark.png?alt=media&token=ffe4a990-3efd-46a3-a021-8a8017cfa7a8'),
    ('sloth', 'https://firebasestorage.googleapis.com/v0/b/plantsnap-419307.appspot.com/o/kanban%2Fsloth.png?alt=media&token=10e76c72-0d65-467c-86c6-4b71e82eb29e'),
    ('weasel', 'https://firebasestorage.googleapis.com/v0/b/plantsnap-419307.appspot.com/o/kanban%2Fweasel.png?alt=media&token=618b152f-ae70-4609-8285-cfd4e220ef88')
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200)
    profile_pic = models.CharField(choices=avatar, default=avatar[0], max_length=200)
    workspace_owner_orders = models.JSONField(default=list, null=True, blank=True)
    workspace_member_orders = models.JSONField(default=list, null=True, blank=True)

    def __str__(self):
        return str(self.user)