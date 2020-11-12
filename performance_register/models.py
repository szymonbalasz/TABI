from django.db import models
from dashboard.models import Project
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date


class SurveillanceOfficer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='surveillance_officer')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Supervisor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='supervisor')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class EvaluationQuestion(models.Model):
    """
    Questions that are found on evaluation survey
    """
    question_text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id} | {self.question_text}"


class SupervisorEvaluation(models.Model):
    questions = models.ManyToManyField(EvaluationQuestion, through="EvaluationAnswer", related_name="evaluation_question")
    date_conducted = models.DateField(default=date.today)
    surveillance_officer = models.ForeignKey(SurveillanceOfficer, on_delete=models.CASCADE,
                                             related_name='supervisor_evaluation')
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)

    def __str__(self):
        return f"Evaluation_ID: {self.id} - {self.surveillance_officer} on {self.date_conducted.month}/{self.date_conducted.year}"


class EvaluationAnswer(models.Model):
    question = models.ForeignKey(EvaluationQuestion, on_delete=models.CASCADE)
    evaluation = models.ForeignKey(SupervisorEvaluation, on_delete=models.CASCADE, related_name='evaluation_answer')
    question_score = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    rating_reason = models.CharField(max_length=255, default="No feedback from supervisor")
    employee_feedback = models.CharField(max_length=255, default="No feedback from employee")

    def __str__(self):
        return f"Question_ID: {self.question.id} on Evaluation_ID: {self.evaluation.id} " \
               f"({self.evaluation.surveillance_officer} - {self.evaluation.surveillance_officer.project})"


class IndividualMonthlyRating(models.Model):
    """
    Individual Performance Scores as obtained from CiiMs, manual performance register and supervisor feedback forms
    """
    surveillance_officer = models.ForeignKey(SurveillanceOfficer, on_delete=models.CASCADE,
                                             related_name='individual_monthly_rating')
    # CiiMs derived
    total_entries = models.PositiveIntegerField()
    total_shifts = models.PositiveIntegerField()
    day_shifts = models.PositiveIntegerField(default=0)
    incidents = models.PositiveIntegerField()
    non_compliances = models.PositiveIntegerField()
    observations = models.PositiveIntegerField()
    covid19_non_compliances = models.PositiveIntegerField(default=0)
    mistakes = models.PositiveIntegerField()
    date = models.DateField()  # any day of month will work - we are only interested in the month

    # Supervisor evaluation
    supervisor_evaluation = models.OneToOneField(SupervisorEvaluation, on_delete=models.CASCADE, default=None,
                                                 blank=True, null=True, related_name='individual_monthly_rating')

    def __str__(self):
        return f"{self.surveillance_officer} {self.date.month}/{self.date.year}"

    @property
    def month(self):
        return f"{self.date.year}/{self.date.month}"

    @property
    def project(self):
        return self.surveillance_officer.project

    @property
    def accuracy_rate(self):
        return round((1 - self.mistakes/self.total_entries) * 100)

    @property
    def total_risks(self):
        return self.incidents + self.non_compliances + self.observations

    @property
    def supervisor_mark(self):
        if self.supervisor_evaluation is None:
            return 0

        scores = [score.question_score * 10.0 for score in self.supervisor_evaluation.evaluation_answer.all()]

        if len(scores) == 0:
            return 0

        mark = round(sum(scores) / len(scores))

        return mark

    @property
    def evaluation(self):
        result = {}
        if self.supervisor_evaluation is None:
            return result

        for question in self.supervisor_evaluation.evaluation_answer.all():
            result[question.question.question_text] = {
                'score': question.question_score,
                'supervisor_feedback': question.rating_reason,
                'employee_feedback': question.employee_feedback,
            }

        return {self.surveillance_officer.__str__(): result}

    def average_group_entries_per_shift(self, day_shift):
        members = IndividualMonthlyRating.objects.filter(
            date__month=self.date.month).filter(
            date__year=self.date.year).filter(
            surveillance_officer__project=self.project
        )
        group_entries_per_shift = [(member.total_entries / (member.day_shifts if day_shift else member.total_shifts))
                                   for member in members]

        return sum(group_entries_per_shift) / len(group_entries_per_shift)

    def weighted_risk_observation_score(self, day_shift=True):
        shifts = self.day_shifts if day_shift else self.total_shifts
        average_own_entries_per_shift = self.total_entries / shifts
        weighted_modifier = average_own_entries_per_shift / self.average_group_entries_per_shift(day_shift)

        risks = self.incidents + self.non_compliances + self.observations
        average_own_risks_per_shift = risks / shifts
        risk_observation_score = average_own_risks_per_shift / average_own_entries_per_shift

        return round(weighted_modifier * risk_observation_score * 100)
