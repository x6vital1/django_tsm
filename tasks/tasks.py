from celery import shared_task
from django.conf import settings

from utils.message_sender import TelegramMessageSender


@shared_task
def send_task_notification(telegram_id, message):
    telegram_sender = TelegramMessageSender(settings.TELEGRAM_BOT_TOKEN)
    telegram_sender.send_message(chat_id=telegram_id, message=message)