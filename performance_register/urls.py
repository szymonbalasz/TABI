from django.urls import path
from . import views

urlpatterns = [
    path('performance_register/', views.performance_register, name='performance_register'),
    path('performance_register/historical/', views.performance_register_historical, name='pr_historical'),
]