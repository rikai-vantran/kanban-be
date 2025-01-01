from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Cards, Workspaces
from api.models import Columns
from utils.cloudinary_upload_services import remove_file

@receiver(post_delete, sender=Cards)
def post_delete_card(sender, instance, **kwargs):
    print(f'{instance.name} has been deleted')
    # remove image from cloudinary
    if instance.image:
        remove_file(instance.id)

@receiver(post_save, sender=Columns)
def post_save_column(sender, instance, created, **kwargs):
    if created:
        # update column order in workspace 
        workspace = instance.workspace
        workspace.column_orders.append(str(instance.id))
        workspace.save()