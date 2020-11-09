from django.urls import path
from . import views

urlpatterns = [
    path('performance_register', views.performance_regiser, name='performance_register'),
]