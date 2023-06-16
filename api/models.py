from django.db import models
from telegram_bot.management.commands.bot import bot
import subprocess
import signal

# Create your models here.
class Bot(models.Model):
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        process = None
        if self.is_active:
            process = subprocess.Popen(["python", "/home/FindEmail/target_directory/FindEmail/manage.py", "bot"])
        elif process is not None:
            process.kill()
        else:
            print(process)
        super().save(*args, **kwargs)