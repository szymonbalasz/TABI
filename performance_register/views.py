from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import models
from dashboard.models import Project
from datetime import date
from .data import get_data


@login_required
def performance_register(request):
    data = get_data(Project.objects.get(id=request.user.user_profile.active_project))
    return render(request, 'performance_register.html', {'data': data})