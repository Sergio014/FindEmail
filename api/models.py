from django.db import models
from telegram_bot.management.commands.monitoring import monitoring_job
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