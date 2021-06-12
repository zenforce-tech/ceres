from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    #path('home/', views.home, name='home'),
]
