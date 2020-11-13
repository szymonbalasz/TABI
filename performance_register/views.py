from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import models
from dashboard.models import Project
from datetime import date
from .data import get_data, get_report_date
from calendar import month_name

@login_required
def performance_register(request):
    report_date = get_report_date(1)
    data = get_data(Project.objects.get(id=request.user.user_profile.active_project), report_date[0], report_date[1])
    return render(request, 'performance_register.html', {'data': data, 'year': report_date[0], 'month': month_name[report_date[1]]})