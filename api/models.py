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
    date = models.DateTimeField()
    description = models.TextField()

    def save(self, *args, **kwargs):
        monitoring_job()
        super().save(*args, **kwargs)