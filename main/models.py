from django.db import models
from django.contrib.auth.models import User

# Create user model to find info buy email
class ExposedUser(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        # how it shows in db
        db_table = 'user'

class TelegramUser(models.Model):
    email = models.EmailField()
    telegram_id = models.BigIntegerField()