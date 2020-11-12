from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, Span
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.embed import components
from .models import IndividualMonthlyRating
from datetime import date

MODIFIER_SUPERVISOR_MARK = 0.6
MODIFIER_WORK_OUTPUT = 0.2
MODIFIER_ACCURACY_RATE = 0.2

MONTH_OPTIONS = {
    'latest': [1],
    'historical:': [1, 2, 3, 4, 5, 6],
}


def get_month(option):
    pass


def performance_report(officers, supervisor_marks, work_outputs, accuracy_rates):
    result = {}
    for i in range(len(officers)):
        final_mark = round(sum([
            supervisor_marks[i] * MODIFIER_SUPERVISOR_MARK,
            work_outputs[i] * MODIFIER_WORK_OUTPUT,
            accuracy_rates[i] * MODIFIER_ACCURACY_RATE,
        ]))
        result[officers[i]] = {
            'supervisor_mark': supervisor_marks[i],
            'work_output': work_outputs[i],
            'accuracy_rate': accuracy_rates[i],
            'final_mark': final_mark,
        }

    return result


def card_stats(report):
    activity = {}
    mark = {}
    accuracy = {}

    for officer, stat in report.items():
        activity[officer] = stat['work_output']
        mark[officer] = stat['final_mark']
        accuracy[officer] = stat['final_mark']

    cards = {
        'most_active': max(activity, key=activity.get),
        'highest_score': max(mark, key=mark.get),
        'lowest_score': min(mark, key=mark.get),
        'most_mistakes': min(accuracy, key=accuracy.get),
    }

    return cards


def get_data(active_project):
    latest_month = date.today().month - 1 if date.today().day > 15 else date.today().month - 3  # CHANGE!
    latest_year = date.today().year
    if latest_month == 0:
        latest_month = 12
        latest_year -= 1
    elif latest_month == -1:
        latest_month = 11
        latest_year -= 1

    ratings = IndividualMonthlyRating.objects.filter(
        surveillance_officer__project=active_project).filter(
        date__month=latest_month).filter(
        date__year=latest_year
    )

    officers, risk_observation_scores, supervisor_marks, accuracy_rates, total_entries, total_risks, evaluations \
        = ([] for i in range(7))

    for rating in ratings:
        officers.append(rating.surveillance_officer.__str__())
        risk_observation_scores.append(rating.weighted_risk_observation_score(day_shift=True))
        supervisor_marks.append(rating.supervisor_mark)
        accuracy_rates.append(rating.accuracy_rate)
        total_entries.append(rating.total_entries)
        total_risks.append(rating.total_risks)
        evaluations.append(rating.evaluation)

    work_outputs = [round(output / max(risk_observation_scores) * 100) for output in risk_observation_scores]

    data = {
        'chart': chart(officers, risk_observation_scores) if len(risk_observation_scores) > 0 else {},
        'performance_report': performance_report(officers, supervisor_marks, work_outputs, accuracy_rates),
        'total_entries_logged': sum(total_entries),
        'total_risks_logged': sum(total_risks),
        'evaluations': evaluations
    }

    data['cards'] = card_stats(data['performance_report'])

    return data


def chart(officers, scores):
    source = ColumnDataSource(data=dict(officers=officers, scores=scores))

    p = figure(x_range=officers, plot_height=350, toolbar_location=None,
               title="Risk Observation Scores per Member (Higher is Better)")
    p.vbar(x='officers', top='scores', width=0.9, source=source,
           line_color='white', fill_color=factor_cmap('officers', palette=Spectral6, factors=officers))

    p.line([], [], legend_label='Group Average', line_color='green', line_dash='dashed')
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.y_range.end = max(scores) * 1.1
    p.legend.orientation = "horizontal"
    p.legend.location = "top_left"

    p.renderers.extend([Span(location=(sum(scores) / len(scores)), dimension='width', line_color='green',
                             line_dash='dashed', line_width=3)])

    script, div = components(p)

    result = {
        'script': script,
        'div': div
    }

    return result
