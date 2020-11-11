from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    projects = models.ManyToManyField(Project)
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100, default='Tarsuis Client')

    _active_project = None

    def __str__(self):
        return f"{self.user.get_full_name()} (User ID: {self.user.id})"

    @property
    def active_project(self):
        if not self._active_project:
            self._active_project = self.projects.all()[0].id
        return self._active_project

    @active_project.setter
    def active_project(self, project_id):
        self._active_project = project_id
