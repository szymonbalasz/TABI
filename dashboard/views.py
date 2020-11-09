from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required()
def home(request):
    return render(request, 'home.html', {})


@login_required()
def coming_soon(request):
    return  render(request, 'coming_soon.html', {})