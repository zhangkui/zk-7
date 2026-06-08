from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import HeritageProject, Exhibition
from .documents import HeritageProjectDocument, ExhibitionDocument


@receiver(post_save, sender=HeritageProject)
def update_project_document(sender, instance, **kwargs):
    try:
        HeritageProjectDocument().update(instance)
    except Exception:
        pass


@receiver(post_delete, sender=HeritageProject)
def delete_project_document(sender, instance, **kwargs):
    try:
        HeritageProjectDocument().delete(instance)
    except Exception:
        pass


@receiver(post_save, sender=Exhibition)
def update_exhibition_document(sender, instance, **kwargs):
    try:
        ExhibitionDocument().update(instance)
    except Exception:
        pass


@receiver(post_delete, sender=Exhibition)
def delete_exhibition_document(sender, instance, **kwargs):
    try:
        ExhibitionDocument().delete(instance)
    except Exception:
        pass
