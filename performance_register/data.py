from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, Span
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.embed import components


def chart(officers, scores):

    source = ColumnDataSource(data=dict(officers=officers, scores=scores))

    p = figure(x_range=officers, plot_height=350, toolbar_location=None, title="Performance Register")
    p.vbar(x='officers', top='scores', width=0.9, source=source,
           line_color='white', fill_color=factor_cmap('officers', palette=Spectral6, factors=officers))

    p.line([], [], legend_label='Average', line_color='green', line_dash='dashed')
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.y_range.end = max(scores)*1.1
    p.legend.orientation = "horizontal"
    p.legend.location = "top_left"

    p.renderers.extend([Span(location=(sum(scores)/len(scores)), dimension='width', line_color='green', line_dash='dashed', line_width=3)])

    script, div = components(p)

    result = {
        'script': script,
        'div': div
    }

    return result
