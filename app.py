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
import boto3
from io import StringIO

# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
app.title = 'Covid-19 Impact Dashboard'
server = app.server


### STYLES
styleH3D = {'color':'#a60f0f'}

### DATA

# get your credentials from environment variables
[AWSID] = 'AKIAYCZC672RTB5662NO'
[YOUR AWS SECRET] = 'TGHCYXGzA4C6p2MVs71CmO8nbCPzBVbM26SaHvwt'

client = boto3.client('s3', aws_access_key_id=[AWSID], [YOUR AWS SECRET]_access_key=[YOUR AWS SECRET])
ABC = 'jbsdc-output'
object_key = 'Corn Prices - 59 Year Historical Chart.csv'
csv_obj = client.get_object(Bucket=ABC, Key=object_key)
body = csv_obj['Body']
csv_string = body.read().decode('utf-8')


df_CornPrices = pd.read_csv(StringIO(csv_string))
## Process Corn Prices
df_CornPrices.dropna(inplace=True)
df_CornPrices['date'] = pd.to_datetime(df_CornPrices['date'], utc=False)
df_CornPrices.index = df_CornPrices['date']
df_CornPrices.drop(['date'], axis = 1, inplace= True)
y_CornPrices = df_CornPrices.resample('MS').mean()
y_CornPrices.fillna(y_CornPrices.bfill())
y_CornPrices = y_CornPrices['2015':]
y_CornPrices = pd.DataFrame(data=y_CornPrices.values, index=y_CornPrices.index, columns=["value"])
#print(y_CornPrices)
## CALCULATION
mod = sm.tsa.statespace.SARIMAX(y_CornPrices,
                            order=(0, 1, 1),
                            seasonal_order=(1, 1, 1, 12),
                            enforce_stationarity=False,
                            enforce_invertibility=False)
results_CornPrices = mod.fit()
pred_dynamic_CornPrices = results_CornPrices.get_prediction(start=pd.to_datetime('2020-01-01'), dynamic=True, full_results=True)
pred_dynamic_ci_CornPrices = pred_dynamic_CornPrices.conf_int()
##DEVELOP CHART 
figCornPrices = go.Figure()
figCornPrices.add_trace(go.Scatter(x=y_CornPrices.index, y=y_CornPrices["value"], mode='lines'))
figCornPrices.add_trace(go.Scatter(x=pred_dynamic_ci_CornPrices.index, y=pred_dynamic_CornPrices.predicted_mean.values, mode='lines'))
figCornPrices.add_shape(dict(type="line", x0=pd.to_datetime('2020-02-01'), y0=0, x1=pd.to_datetime('2020-02-01'), y1=pred_dynamic_ci_CornPrices.iloc[:, 1].values.max(), line=dict(color="Red", width=3  )))
figCornPrices.add_trace(go.Scatter(x=pred_dynamic_ci_CornPrices.index, y=pred_dynamic_ci_CornPrices.iloc[:, 0], fill='tonexty', mode='lines', line_color='#d4d3d2')) # fill down to xaxis
figCornPrices.add_trace(go.Scatter(x=pred_dynamic_ci_CornPrices.index, y=pred_dynamic_ci_CornPrices.iloc[:, 1], fill='tonexty', mode='lines', line_color='#d4d3d2')) # fill to trace0 y
figCornPrices.update_layout(showlegend=False)
figCornPrices.update_layout(autosize=False, width=300, height=150, margin=dict(l=10, r=10, b=10, t=10, pad=1))




df_OilPrices = pd.read_csv('data/Crude Oil Prices_ Daily Closing Values.csv')
## Process Oil Prices
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
##DEVELOP CHART 
figOilPrices = go.Figure()
figOilPrices.add_trace(go.Scatter(x=y_OilPrices.index, y=y_OilPrices['price'], mode='lines'))
figOilPrices.add_trace(go.Scatter(x=pred_dynamic_ci_OilPrices.index, y=pred_dynamic_OilPrices.predicted_mean.values, mode='lines'))
figOilPrices.add_shape(dict(type="line", x0=pd.to_datetime('2020-02-01'), y0=0, x1=pd.to_datetime('2020-02-01'), y1=pred_dynamic_ci_OilPrices.iloc[:, 1].values.max(), line=dict(color="Red", width=3  )))
figOilPrices.add_trace(go.Scatter(x=pred_dynamic_ci_OilPrices.index, y=pred_dynamic_ci_OilPrices.iloc[:, 0], fill='tonexty', mode='lines', line_color='#d4d3d2')) # fill down to xaxis
figOilPrices.add_trace(go.Scatter(x=pred_dynamic_ci_OilPrices.index, y=pred_dynamic_ci_OilPrices.iloc[:, 1], fill='tonexty', mode='lines', line_color='#d4d3d2')) # fill to trace0 y
figOilPrices.update_layout(showlegend=False)
figOilPrices.update_layout(autosize=False, width=300, height=150, margin=dict(l=10, r=10, b=10, t=10, pad=1))



## LAYOUT DESIGN
#app.layout = html.Div(children=[dcc.Graph(figure=fig)])

app.layout = html.Div(className="body",
    children=[
        html.H2("Covid-19 impact dashboard"), 
        html.Div(className="row",
        children=[
            html.Div(className="columnleft",
            children=[
                html.H3("Demand impact", style=styleH3D),
                html.Table(className="center",
                    children=[
                        html.Tr(
                            children=[
                                html.Td(
                                    children=[
                                        html.P("Oil Prices"),
                                        dcc.Graph(figure=figOilPrices)
                                    ]
                                ),
                                html.Td(
                                    children=[
                                        html.P("Corn Prices"),
                                        dcc.Graph(figure=figCornPrices)
                                    ]
                                )
                            ]
                        ),
                        html.Tr(
                            children=[
                                html.Td(
                                    children=[
                                        html.P("Soy bean prices"),
                                        dcc.Graph(figure=figOilPrices)
                                    ]
                                ),
                                html.Td(
                                    children=[
                                        html.P("Rice prices"),
                                        dcc.Graph(figure=figCornPrices)
                                    ]
                                )
                            ]                            
                        )
                    ]
                )
            ]),
            html.Div(className="columnright",
            children=[
                html.H3("Supply impact"),
                html.Table(
                    children=[
                        html.Tr(
                            children=[
                                html.Td(
                                    children=[
                                        html.P("a")
                                    ]
                                ),
                                html.Td(
                                    children=[
                                        html.P("b")
                                    ]
                                )
                            ]
                        ),
                        html.Tr(
                            children=[
                                html.Td(
                                    children=[
                                        html.P("c")
                                    ]
                                ),
                                html.Td(
                                    children=[
                                        html.P("d")
                                    ]
                                )
                            ]                            
                        )
                    ]
                )
            ])            
        ])
    ])

## CALLBACKS (to update the charts)

if __name__ == '__main__':
    app.run_server(debug=True)
