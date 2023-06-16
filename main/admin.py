from django.contrib import admin
from .models import *

# register user model in admin panel
admin.site.register(User)