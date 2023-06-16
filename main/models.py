from django.db import models

# Create user model to find info buy email
class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        # how it shows in db
        db_table = 'user'