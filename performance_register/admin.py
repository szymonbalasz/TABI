from django.contrib import admin
from .models import SurveillanceOfficer, Supervisor, IndividualMonthlyRating, EvaluationQuestion, SupervisorEvaluation, EvaluationAnswer


class SurveillanceOfficerAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'id', 'project']
    list_filter = ['project']
    search_fields = ['first_name', 'last_name']


class SupervisorAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'id', 'project']
    list_filter = ['project']
    search_fields = ['first_name', 'last_name']


class EvaluationQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'id']


class SupervisorEvaluationAdmin(admin.ModelAdmin):
    list_display = ['id', 'surveillance_officer', 'date_conducted']


class EvaluationAnswerAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'question_score', 'id']
    list_filter = ['evaluation__surveillance_officer', 'evaluation__surveillance_officer__project']
    date_hierarchy = 'evaluation__date_conducted'


class IndividualMonthlyRatingAdmin(admin.ModelAdmin):
    list_display = ['surveillance_officer', 'id', 'month', 'project']
    search_fields = ['surveillance_officer__first_name', 'surveillance_officer__last_name']
    date_hierarchy = 'date'
    list_filter = ['surveillance_officer__project']


admin.site.register(SurveillanceOfficer, SurveillanceOfficerAdmin)
admin.site.register(IndividualMonthlyRating, IndividualMonthlyRatingAdmin)
admin.site.register(Supervisor, SupervisorAdmin)
admin.site.register(EvaluationQuestion, EvaluationQuestionAdmin)
admin.site.register(SupervisorEvaluation, SupervisorEvaluationAdmin)
admin.site.register(EvaluationAnswer, EvaluationAnswerAdmin)