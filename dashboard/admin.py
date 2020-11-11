from django.contrib import admin
from .models import Project, UserProfile

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']

admin.site.register(Project, ProjectAdmin)
admin.site.register(UserProfile)
