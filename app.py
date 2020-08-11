import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output
import json
from urllib.request import urlopen
import datetime as dt
from datetime import datetime, timedelta
import numpy as np
import statsmodels.api as sm

# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
app.title = 'Displacement visualization tool'
server = app.server


### DATA
Oil = pd.read_csv('data/Crude Oil Prices_ Daily Closing Values.csv')
Broiler = pd.read_csv('data/SlaughterCounts-Broilers.csv')

## APPLICATION START

## LAYOUT DESIGN
app.layout = html.Div(children=[html.P('Hello')])


## CALLBACKS (to update the charts)

if __name__ == '__main__':
    app.run_server(debug=False)
