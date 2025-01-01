from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Workspaces
        
@receiver(post_save, sender=Workspaces)
def post_save_workspace(sender, instance, created, **kwargs):
    if created:
        # Add init column in workspace
        instance.columns_set.create(name='To Do', card_orders=[])
        instance.columns_set.create(name='In Progress', card_orders=[])
        instance.columns_set.create(name='Done', card_orders=[])

        # Add init label in workspace
        instance.labels_set.create(name='High', color='#f87168')
        instance.labels_set.create(name='Medium', color='#f5cd47')
        instance.labels_set.create(name='Low', color='#4bce97')