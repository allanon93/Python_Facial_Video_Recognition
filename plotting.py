from script import data
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

data["Start_string"] = data["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
data["Stop_string"] = data["Stop"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds = ColumnDataSource(data)

p = figure(x_axis_type = 'datetime', height = 100, width = 500,
sizing_mode = "stretch_width", title = "Motion Graph")

p.yaxis.minor_tick_line_color = None
p.yaxis[0].ticker.desired_num_ticks = 1

hover = HoverTool(tooltips = [("Start", "@Start_string"), ("Stop", "@Stop_string")])

p.add_tools(hover)

q = p.quad(left = "Start", right = "Stop", bottom = 0, top = 1,
color = 'Green', source = cds)

output_file("Motion_Graph.html")
show(p)
