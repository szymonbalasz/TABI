from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:project_id>/', views.home),
    path('coming_soon/', views.coming_soon, name='coming_soon'),
    path('accounts/', include('django.contrib.auth.urls')),
]