from django.db import models
from telegram_bot.management.commands.monitoring import monitoring_job
from telegram_bot.management.commands.bot import delete_message_from_user
import subprocess
import signal


# Create your models here.
class Bot(models.Model):
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        process = subprocess.Popen(["python", "/home/FindEmail/target_directory/FindEmail/manage.py", "bot"])
        if not self.is_active:
            process.kill()
        super().save(*args, **kwargs)

class Monitoring(models.Model):
    USER_CHOICES = [
        ('all', 'Start monitoring for all users'),
        ('email_group', 'Start monitoring for specific group of checked email users'),
        ('hwid_group', 'Start monitoring for specific group of checked HWID users'),
    ]

    description = models.TextField()
    kind = models.CharField(max_length=11, choices=USER_CHOICES)
    group = models.ForeignKey(to='main.CustomGroup', on_delete=models.SET_NULL, null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.kind == 'all':
            monitoring_job()
        elif self.kind == 'email_group':
            monitoring_job(self.group, 'email')
        elif self.kind == 'hwid_group':
            monitoring_job(self.group, 'hwid')
        super().save(*args, **kwargs)

class NotificationHistory(models.Model):
    text = models.TextField()
    telegram_id = models.BigIntegerField()
    date_of_sending = models.DateTimeField(auto_now_add=True)
    message_id = models.BigIntegerField()

    def delete(self, *args, **kwargs):
        delete_message_from_user(self.telegram_id, self.message_id)
        super().delete(*args, **kwargs)

class Rating(models.Model):
    stars = models.IntegerField()

    @property
    def calculate_average_rating(self):
        total_ratings = self.__class__.objects.aggregate(models.Avg('stars'))
        return round(total_ratings['stars__avg'], 1)