from datetime import timedelta
from django.utils.timezone import now

from .models import Tasks
from .tasks import send_task_notification
from utils.static_text import task_notification, task_created


def send_reminders(task):
    deadline = task.deadline
    reminders = [
        (deadline - timedelta(days=1), task_notification(task, "1 день")),
        (deadline - timedelta(hours=12), task_notification(task, "12 часов")),
        (deadline - timedelta(hours=6), task_notification(task, "6 часов")),
        (deadline - timedelta(hours=3), task_notification(task, "3 часа")),
        (deadline - timedelta(hours=1), task_notification(task, "1 час")),
    ]
    for reminder_time, message in reminders:
        if reminder_time > now():
            send_task_notification.apply_async((task.user.telegram_id, message), eta=reminder_time)

def send_created_notification(task):
    task = Tasks.objects.get(id=task.id)
    send_task_notification.delay(task.user.telegram_id, task_created(task))
