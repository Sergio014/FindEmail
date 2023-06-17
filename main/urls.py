from django.urls import path
from . import views

urlpatterns = [
    # for sending email activation to email
    # path('', views.activate_email_view, name='activate_email'),
    # send data to check
    path('<telegram_id>', views.check_full_data),
    # to activate email
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]