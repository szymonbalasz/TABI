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

    def __str__(self):
        return f"{self.user.get_full_name()}"

    @property
    def default_project(self):
        if self.projects:
            return self.projects.get(id=1)