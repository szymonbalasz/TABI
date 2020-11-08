from django.contrib import admin
from .models import SurveillanceOfficer, Supervisor, IndividualMonthlyRating, EvaluationQuestion, SupervisorEvaluation, EvaluationAnswer


class SurveillanceOfficerAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'id', 'project']
    list_filter = ['project']
    search_fields = ['first_name', 'last_name']


class IndividualMonthlyRatingAdmin(admin.ModelAdmin):
    list_display = ['surveillance_officer', 'month', 'project']
    search_fields = ['surveillance_officer__first_name', 'surveillance_officer__last_name']
    date_hierarchy = 'date'
    list_filter = ['surveillance_officer__project__name']


admin.site.register(SurveillanceOfficer, SurveillanceOfficerAdmin)
admin.site.register(IndividualMonthlyRating, IndividualMonthlyRatingAdmin)
admin.site.register(Supervisor)
admin.site.register(EvaluationQuestion)
admin.site.register(SupervisorEvaluation)
admin.site.register(EvaluationAnswer)