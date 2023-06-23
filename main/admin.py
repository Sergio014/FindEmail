from django.contrib import admin
from .models import *

# register models in admin panel
admin.site.register(Credential)

admin.site.register(PCinfo)

admin.site.register(RandomData)

admin.site.register(CheckedEmailUser)

admin.site.register(CustomGroup)