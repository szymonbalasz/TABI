from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html', {})


def coming_soon(request):
    return  render(request, 'coming soon.html', {})