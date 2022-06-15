from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.data_base, name='index'),
    ]