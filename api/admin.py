from django.contrib import admin
from .models import *

# Register bot model to manage telegram bot through admin panel
admin.site.register(Monitoring)

admin.site.register(Bot)