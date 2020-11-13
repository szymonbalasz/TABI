from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required()
def home(request, project_id=None):
    if project_id is not None:
        if int(project_id) in [project.id for project in request.user.user_profile.projects.all()]:
            request.user.user_profile.active_project = int(project_id)
        return redirect(home)
    return render(request, 'home.html', {})


@login_required()
def coming_soon(request):
    return render(request, 'coming_soon.html', {})