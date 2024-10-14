def task_expired_notification(task, damage):
    message = (f"💀 КВЕСТ НЕ ВЫПОЛНЕН! 💀\n"
               "----------------------------------------------\n"
               f"❌ Задача: {task.title}\n"
               f"💀 Урон: {damage} ❤️\n"
               f"❤️ Здоровье: {task.user.userprofile.health_points} ❤️\n"
               "----------------------------------------------\n"
               "⚔️ Ты не смог завершить задание. Здоровье не восстанавливается!"
               )
    return message
