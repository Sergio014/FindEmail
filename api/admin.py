from django.contrib import admin
from .models import *

# Register bot model to manage telegram bot through admin panel
class StarsAdmin(admin.ModelAdmin):
    list_display = ('stars', 'calculate_average_rating')
    readonly_fields = ('calculate_average_rating',)

admin.site.register(Rating, StarsAdmin)

admin.site.register(NotificationHistory)

admin.site.register(Monitoring)

admin.site.register(Bot)