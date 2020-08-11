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
import warnings
warnings.filterwarnings("ignore")

# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
app.title = 'Displacement visualization tool'
server = app.server


### DATA
df_OilPrices = pd.read_csv('data/Crude Oil Prices_ Daily Closing Values.csv')

## APPLICATION START
df_OilPrices.dropna(inplace=True)
df_OilPrices['date'] = pd.to_datetime(df_OilPrices['date'], utc=False)
df_OilPrices.index = df_OilPrices['date']
df_OilPrices.drop(['date'], axis = 1, inplace= True)
y_OilPrices = df_OilPrices.resample('MS').mean()
y_OilPrices.fillna(y_OilPrices.bfill())
y_OilPrices = y_OilPrices['2015':]

## DEVELOP CHART
OilPrices = px.line(df_OilPrices, x=df_OilPrices.index, y=df_OilPrices['price'])
OilPrices.update_layout({'height': 200, 'width': 400})

## LAYOUT DESIGN
app.layout = html.Div(children=[dcc.Graph(figure=OilPrices)])


## CALLBACKS (to update the charts)

if __name__ == '__main__':
    app.run_server(debug=False)
