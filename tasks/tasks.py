from celery import shared_task
from django.conf import settings
from django.utils.timezone import now

from tasks.models import Tasks
from users.utils.damage_calculator import DefaultDamageCalculator
from utils.message_sender import TelegramMessageSender
from utils.static_text import task_expired_notification


@shared_task
def send_task_notification(telegram_id, message):
    telegram_sender = TelegramMessageSender(settings.TELEGRAM_BOT_TOKEN)
    telegram_sender.send_message(chat_id=telegram_id, message=message)


@shared_task
def check_deadlines():
    expired_tasks = Tasks.objects.filter(deadline__lt=now(), completed=False, status=Tasks.STATUS_PENDING)
    for task in expired_tasks:
        task.status = Tasks.STATUS_EXPIRED
        damage = DefaultDamageCalculator().calculate(task.difficulty)
        task.miss_deadline(damage)
        task.save()
        send_task_notification.delay(task.user.telegram_id, task_expired_notification(task, damage))
