import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px

import pandas as pd
import statsmodels.api as sm
# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
app.title = 'Displacement visualization tool'
server = app.server

## APPLICATION START

## LAYOUT DESIGN
app.layout = html.Div(className="row",
    children=[html.P('Hello World 1')])




if __name__ == '__main__':
    app.run_server(debug=False)