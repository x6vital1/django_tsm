from django.db import models
from django.utils import timezone

from users.models import CustomUser, UserProfile
from utils.models import CreateUpdateTracker, nb, GetOrNoneManager

from users.utils.damage_calculator import DefaultDamageCalculator


class Tasks(CreateUpdateTracker):
    title = models.CharField(max_length=255, **nb)
    description = models.TextField(**nb)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    DIFFICULTY_EASY = 10
    DIFFICULTY_MEDIUM = 20
    DIFFICULTY_HARD = 30
    DIFFICULTY_CHOICES = (
        (DIFFICULTY_EASY, 'Easy'),
        (DIFFICULTY_MEDIUM, 'Medium'),
        (DIFFICULTY_HARD, 'Hard'),
    )

    STATUS_COMPLETED = 'completed'
    STATUS_PENDING = 'pending'
    STATUS_EXPIRED = 'expired'
    STATUS_CHOICES = (
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_PENDING, 'Pending'),
        (STATUS_EXPIRED, 'Expired'),
    )

    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, **nb)
    deadline = models.DateTimeField(**nb)
    status = models.CharField(choices=STATUS_CHOICES, default=STATUS_PENDING, max_length=30, **nb)
    completed = models.BooleanField(default=False)

    objects = GetOrNoneManager()

    def __str__(self):
        return f'{self.title} - {self.difficulty}'

    def complete_task(self):
        self.completed = True
        self.user.exp_points += self.difficulty
        self.user.save()

    def miss_deadline(self, damage):
        if not self.completed:
            self.user.userprofile.reduce_health_points(damage)

