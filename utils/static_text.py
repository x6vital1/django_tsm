def task_notification(task, deadline):
    message = (
        f"🔔 Напоминание о задаче: {task.title}\n"
        "----------------------------------------------\n"
        f"Осталось {deadline} до дедлайна!\n"
        f"Описание: {task.description}\n"
        f"Время дедлайна: {task.deadline.strftime('%Y-%m-%d %H:%M')}\n"
        f"Сложность задачи: {task.difficulty} ❤️\n"
        "----------------------------------------------\n"
    )
    return message

def task_created(task):
    message = (
        f"📝 НОВАЯ ЗАДАЧА: {task.title}\n"
        "----------------------------------------------\n"
        f"Описание: {task.description}\n"
        f"Сложность задачи: {task.difficulty} ❤️\n"
        f"Время дедлайна: {task.deadline.strftime('%Y-%m-%d %H:%M')}\n"
        "----------------------------------------------\n"
    )
    return message