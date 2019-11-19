from django.urls import path
from . import views

urlpatterns = [
    path('', views.to_main, name='home'),
    path('main/',views.mainpage, name='home-main'),
    path('ajax/load-categories/', views.load_cat, name='ajax-load-categories'),
]
