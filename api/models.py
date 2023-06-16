from django.db import models

# Create your models here.
class Bot(models.Model):
    is_active = models.BooleanField(default=True)