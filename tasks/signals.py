from django.db.models.signals import post_save
from django.dispatch import receiver

from tasks.models import Tasks
from users.utils.notification_utils import TasksNotificationSender


@receiver(post_save, sender=Tasks)
def send_task_notification(sender, instance, created, **kwargs):
    if created:
        TasksNotificationSender(instance).create_notification()
        TasksNotificationSender(instance).deadline_reminders()