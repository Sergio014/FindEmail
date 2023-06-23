from django.db import models
from django.contrib.auth.models import User

class CheckedEmailUser(models.Model):
    email = models.EmailField()
    telegram_id = models.BigIntegerField()
    found = models.BooleanField(default=False)
    checked_at = models.DateField(auto_now_add=True)

class CheckedHWIDUser(models.Model):
    HWID = models.CharField(max_length=255)
    telegram_id = models.BigIntegerField()
    found = models.BooleanField(default=False)
    checked_at = models.DateField(auto_now_add=True)

class Credential(models.Model):
    folder_name = models.CharField(max_length=255)
    url = models.URLField()
    username = models.EmailField()
    password = models.CharField(max_length=255)

class PCinfo(models.Model):
    folder_name = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    path_to_virus = models.CharField(max_length=255)
    username = models.EmailField()
    HWID = models.CharField(max_length=255)
    operating_system = models.CharField(max_length=255)
    date_log = models.DateTimeField(auto_now_add=True)
    file_list = models.CharField(max_length=255)

class RandomData(models.Model):
    url = models.URLField()
    username = models.EmailField()
    password = models.CharField(max_length=255)
    exposed_at = models.DateTimeField(auto_now_add=True)

class CustomGroup(models.Model):
    # Add any additional fields or properties you want for your custom group model
    email_notifications = models.BooleanField()
    PC_notifications = models.BooleanField()
    need_to_verify = models.BooleanField()
    users = models.ManyToManyField(CheckedEmailUser)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)