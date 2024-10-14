from django.db import models
from users.models.custom_user import CustomUser
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    exp_points = models.IntegerField(default=0)
    health_points = models.IntegerField(default=100)

    def __str__(self):
        return f'{self.user.username} - level {self.level}'

    def add_exp_points(self, points):
        self.exp_points += points
        self.save()

    def reduce_health_points(self, points):
        self.health_points -= points
        self.save()
        if self.health_points <= 0:
            self.reset_user()

    def reset_user(self):
        self.health_points = 100
        self.exp_points = 0
        self.level = 0
        self.save()

    def check_level_up(self):
        if self.exp_points >= 100:
            self.level += 1
            self.health_points = 100
            self.exp_points = 0
            self.save()