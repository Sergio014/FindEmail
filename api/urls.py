from django.urls import path
from . import views

urlpatterns = [
    path('check_bot', views.check_bot_view),
    path('check/<email>/<telegram_id>', views.check_email),
]