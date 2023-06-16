from django.db import models
from telegram_bot.management.commands.bot import bot


# Create your models here.
class Bot(models.Model):
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.is_active:
            bot.infinity_polling()
        else:
            bot.stop_bot()
        super().save(*args, **kwargs)