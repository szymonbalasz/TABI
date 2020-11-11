from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import models
from datetime import date
from .data import chart

@login_required
def performance_register(request):
    latest_month = date.today().month-1 if date.today().day > 15 else date.today().month-3
    if latest_month == 0:
        latest_month = 12
    elif latest_month == -1:
        latest_month = 11

    active_project = request.user.user_profile.active_project
    ratings = models.IndividualMonthlyRating.objects.filter(
        surveillance_officer__project=active_project).filter(
        date__month=latest_month).filter(
        date__year=date.today().year
    )

    names = [rating.surveillance_officer.__str__() for rating in ratings]
    scores = [rating.weighted_risk_observation_score()*100 for rating in ratings]

    graph = chart(names, scores)

    return render(request, 'performance_register.html', {'graph' : graph})