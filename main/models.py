from django.db import models
from .activate_email import activate_email

class CheckedEmailUser(models.Model):
    email = models.EmailField()
    telegram_id = models.BigIntegerField()
    found = models.BooleanField(default=False)
    checked_at = models.DateField(auto_now_add=True)
    need_to_verify = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    receive_email_notifications = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.need_to_verify and not self.verified:
            activate_email(self, self.email)
        super().save(*args, **kwargs)

class CheckedHWIDUser(models.Model):
    HWID = models.CharField(max_length=255)
    telegram_id = models.BigIntegerField()
    found = models.BooleanField(default=False)
    checked_at = models.DateField(auto_now_add=True)
    receive_hwid_notifications = models.BooleanField(default=False)

class Credential(models.Model):
    folder_name = models.CharField(max_length=255)
    url = models.URLField()
    username = models.EmailField()
    password = models.CharField(max_length=255)

class PCinfo(models.Model):
    folder_name = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    path_to_virus = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    HWID = models.CharField(max_length=255)
    operating_system = models.CharField(max_length=255)
    date_log = models.DateTimeField(auto_now_add=True)
    file_list = models.CharField(max_length=255)
    checked = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)

class RandomData(models.Model):
    url = models.URLField()
    username = models.EmailField()
    password = models.CharField(max_length=255)
    exposed_at = models.DateTimeField(auto_now_add=True)
    checked = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)

class CustomGroup(models.Model):
    # Add any additional fields or properties you want for your custom group model
    name = models.CharField(max_length=255)
    email_notifications = models.BooleanField()
    PC_notifications = models.BooleanField()
    need_to_verify = models.BooleanField()
    email_users = models.ManyToManyField(CheckedEmailUser, blank=True)
    hwid_users = models.ManyToManyField(CheckedHWIDUser, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for user in self.email_users.all():
            if self.email_notifications:
                user.receive_email_notifications = True
            if self.need_to_verify:
                user.need_to_verify = True
            user.save()
        for user in self.hwid_users.all():
            if self.PC_notifications:
                user.receive_hwid_notifications = True
            user.save()