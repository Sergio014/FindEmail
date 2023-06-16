from django.urls import path
from . import views

urlpatterns = [
    path('check/<email>', views.check_email),
]