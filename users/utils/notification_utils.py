from datetime import timedelta, datetime
from typing import List, Tuple

from django.utils.timezone import now

from tasks.models import Tasks
from tasks.tasks import send_task_notification


class CreateNotification:
    def __init__(self, tasks: Tasks):
        self.tasks = tasks

    def create_message(self) -> str:
        message = (
            f"⚔️ У ТЕБЯ НОВОЕ ЗАДАНИЕ! ⚔️\n"
            "----------------------------------------------\n"
            f"🔹 Задание: {self.tasks.title}\n"
            f"📜 Описание: {self.tasks.description}\n"
            f"💀 Сложность: {self.tasks.difficulty} ❤️\n"
            f"📆 Срок выполнения: {self.tasks.deadline.strftime('%Y-%m-%d %H:%M')}\n"
            "----------------------------------------------\n"
        )
        return message


class DeadlineNotifications:
    def __init__(self, tasks: Tasks):
        self.tasks = tasks

    def deadline_message(self, time_left: str) -> str:
        message = (
            f"⏰ НАПОМИНАНИЕ: ЗАДАНИЕ В ПРОЦЕССЕ! ⏰\n"
            "----------------------------------------------\n"
            f"📝 Задание: {self.tasks.title}\n"
            f"⏳ Осталось времени: {time_left}\n"
            "----------------------------------------------\n"
        )
        return message

    def reminders_generator(self) -> List[Tuple[datetime, str]]:
        reminders_list = [
            (self.tasks.deadline - timedelta(days=1), self.deadline_message("1 день")),
            (self.tasks.deadline - timedelta(hours=12), self.deadline_message("12 часов")),
            (self.tasks.deadline - timedelta(hours=6), self.deadline_message("6 часов")),
            (self.tasks.deadline - timedelta(hours=3), self.deadline_message("3 часа")),
            (self.tasks.deadline - timedelta(hours=1), self.deadline_message("1 час")),
        ]
        return reminders_list


class TasksNotificationSender:
    def __init__(self, tasks: Tasks):
        self.tasks = tasks

    def deadline_reminders(self):
        reminders = DeadlineNotifications(self.tasks).reminders_generator()
        for reminder_time, message in reminders:
            if reminder_time > now():
                send_task_notification.apply_async((self.tasks.user.telegram_id, message), eta=reminder_time)

    def create_notification(self):
        message = CreateNotification(self.tasks).create_message()
        send_task_notification.delay((self.tasks.user.telegram_id, message), eta=self.tasks.deadline)
