from django.shortcuts import render

def performance_regiser(request):
    return render(request, 'performance_register.html', {})