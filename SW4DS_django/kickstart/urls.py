from django.urls import path
from . import views

urlpatterns = [
    path('', views.to_main, name='home'),


]
