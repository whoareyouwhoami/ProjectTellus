from django.urls import path
from . import views

urlpatterns = [
    path('main/',views.mainpage, name='home-main'),
]
