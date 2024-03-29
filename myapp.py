#All the required packages are imported.
import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.layouts import row, widgetbox, gridplot
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput, Div
from bokeh.plotting import figure

#Importing the proj file which will perform the background tasks.
import proj

#List of different ratings metrix that will display for each movie.
movies = ['TEXT BLOB', 'NLTK', 'IMDB']

#Initial value for each ratinf metrix.
rating = [0.0, 0.0, 0.0]

#Source to display the collect data in the graph.
source = ColumnDataSource(data=dict(movies=movies, rating=rating))

#Create a figure that display the rating values.
plot = figure(x_range=movies, plot_height=250, title=" Movie Rating",
           toolbar_location=None, tools="")

#We choose vbar graph to populate the movie rating.
plot.vbar(x='movies', top='rating', source=source, width=0.5)

plot.xgrid.grid_line_color = '#e2e2e2'
plot.y_range.start = 0


xRange = ['NLTK', 'TEXT BLOB']
years = ["Negative", "Positive"]
colors = ["#c9d9d3", "#718dbf"]

data = {'xRange' : xRange,
        'Negative'   : [0, 0],
        'Positive'   : [0, 0],
        }
#Source to display the collected data in the graph.
countSource = ColumnDataSource(data=data)

#Create a figure that display the positive and negative count for NLTK and textblob.
p = figure(x_range=xRange, plot_height=500, title=" Positive and Negative Tweets",
           toolbar_location=None, tools="")

#We choose vbar graph to populate the positive and negative counts.
p.vbar_stack(years, x='xRange', width=0.4, color=colors, source=countSource,
             legend=years)

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = "top_right"
p.legend.orientation = "horizontal"


#TextInout is a widget that is used to collect the movie name from the user.
text = TextInput(title="Search Query:", placeholder='Enter Movie Name',width = 300)


# This function is used to collect the movie name and populate its rating after analysis.
# Once the movie name is collected, this method will proj method to collect the data from twitter, IMDB.
# Once the rating is determined, it is populated in the graph.
def update_title(attrname, old, new):
    proj.searchTwitter(text.value)
    val = proj.getMovieFromDB(text.value)
    plot.title.text = text.value + " Movie Rating"
    p.title.text = text.value + " Positive and Negative Tweets"
    rating = [val[0][1],val[0][2],val[0][3],val[0][4]]
    source.data = dict(movies=movies, rating=rating) 
    data['Negative'] = [val[0][6],val[0][8]]
    data['Positive'] = [val[0][5],val[0][7]]
    countSource.data = data

# This is the event listener that will invoke the method on Enter.
text.on_change('value', update_title)

# This is a HTML tag to display the project title.
head = Div(text="""<h1 align="center" style="color:#1DA1F2;"> TweeRate </h1>""",
width=1500, height=40)

# This HTML tag is used to display the project description.
info = Div(text="""<div style="text-align: center;"><b>From tweetting to rating.</b></div>""",
width=1500, height=40)

# This is provided to give text input examples for the user.
div = Div(text="""Ex: A Quiet Place, Thor...""",
width=800, height=50)


# All the widget are collected as input.
inputs = widgetbox(head, info, text, div)

# Plot the graph in grid system.
grid = gridplot([plot, p], ncols=2, plot_width=700, plot_height=400)

# Add all the elements that is used in the project to display on the web page.
curdoc().add_root(column(inputs, grid))
#curdoc().add_root(column(button, p))
curdoc().title = "TweeRate"