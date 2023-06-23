from django.urls import path
from . import views

urlpatterns = [
    path('check_data', views.check_full_data),
    path('check/<email>/<telegram_id>', views.check_email),
]