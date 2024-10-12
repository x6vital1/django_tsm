from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.reminders import send_reminders, send_created_notification

from tasks.models import Tasks


@receiver(post_save, sender=Tasks)
def send_task_notification(sender, instance, created, **kwargs):
    if created:
        send_created_notification(instance)
        send_reminders(instance)