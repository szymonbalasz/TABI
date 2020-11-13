from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import models
from dashboard.models import Project
from datetime import date
from .data import get_data, get_report_date, mistakes_pie_chart
from calendar import month_name

@login_required
def performance_register(request):
    report_date = get_report_date(1)
    data = get_data(Project.objects.get(id=request.user.user_profile.active_project), report_date[0], report_date[1])
    return render(request, 'performance_register.html', {
        'data': data,
        'year': report_date[0],
        'month': month_name[report_date[1]]
    })

@login_required
def performance_register_historical(request):
    report_one = get_report_date(2)
    report_two = get_report_date(1)
    data_one = get_data(Project.objects.get(id=request.user.user_profile.active_project), report_one[0], report_one[1])
    data_two = get_data(Project.objects.get(id=request.user.user_profile.active_project), report_two[0], report_two[1])

    return render(request, 'performance_register_historical.html', {
        'data_one': data_one,
        'data_two': data_two,
        'year_one': report_one[0],
        'month_one': month_name[report_one[1]],
        'year_two': report_two[0],
        'month_two': month_name[report_two[1]],
    })