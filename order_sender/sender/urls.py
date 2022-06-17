from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.data_base, name='index'),
    path('processing/', views.processing_list, name='processing'),
    path('shipped/', views.shipped_list, name='shipped'),
    path('completed/', views.completed_list, name='completed'),
    path('hole/', views.hole_list, name='hole'),
    ]