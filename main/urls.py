from django.urls import path
from . import views

urlpatterns = [
    # for sending email activation to email
    path('', views.activate_email_view, name='activate_email'),
    # for waiting page
    path('wait/<email>', views.waiting, name='waiting'),
    # to activate email
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]