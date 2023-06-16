from django.contrib import admin
from .models import *

# register models in admin panel
admin.site.register(User)

admin.site.register(TelegramUser)