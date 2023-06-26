from django.urls import path
from . import views

urlpatterns = [
    path('check_data', views.check_full_data),
    path('add_rating', views.add_rating)
]