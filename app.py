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
app.title = 'Covid-19 Impact Dashboard'
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

## CALCULATION
mod = sm.tsa.statespace.SARIMAX(y_OilPrices,
                            order=(0, 1, 1),
                            seasonal_order=(1, 1, 1, 12),
                            enforce_stationarity=False,
                            enforce_invertibility=False)
results_OilPrices = mod.fit()
pred_dynamic_OilPrices = results_OilPrices.get_prediction(start=pd.to_datetime('2020-01-01'), dynamic=True, full_results=True)
pred_dynamic_ci_OilPrices = pred_dynamic_OilPrices.conf_int()

## DEVELOP CHART
OilPrices = px.line(df_OilPrices, x=y_OilPrices.index, y=y_OilPrices['price'])
OilPrices.update_layout({'height': 200, 'width': 400})

fig = go.Figure()
fig.add_trace(go.Scatter(x=y_OilPrices.index, y=y_OilPrices['price'], mode='lines'))
fig.add_trace(go.Scatter(x=pred_dynamic_ci_OilPrices.index, y=pred_dynamic_OilPrices.predicted_mean.values, mode='lines'))
fig.add_shape(dict(type="line", x0=pd.to_datetime('2020-02-01'), y0=0, x1=pd.to_datetime('2020-02-01'), y1=pred_dynamic_ci_OilPrices.iloc[:, 1].values.max(), line=dict(color="Red", width=3  )))
fig.add_trace(go.Scatter(x=pred_dynamic_ci_OilPrices.index, y=pred_dynamic_ci_OilPrices.iloc[:, 0], fill='tonexty', mode='lines', line_color='#d4d3d2')) # fill down to xaxis
fig.add_trace(go.Scatter(x=pred_dynamic_ci_OilPrices.index, y=pred_dynamic_ci_OilPrices.iloc[:, 1], fill='tonexty', mode='lines', line_color='#d4d3d2')) # fill to trace0 y
fig.update_layout(showlegend=False)
fig.update_layout(autosize=False, width=400, height=200, margin=dict(l=10, r=10, b=10, t=10, pad=1))



## LAYOUT DESIGN
#app.layout = html.Div(children=[dcc.Graph(figure=fig)])

app.layout = html.Div(className="body",
    children=[
        html.H2("Covid-19 impact dashboard"), 
        html.Div(
        children=[
            html.Div(className="row")
        ])
    ])

## CALLBACKS (to update the charts)

if __name__ == '__main__':
    app.run_server(debug=True)
