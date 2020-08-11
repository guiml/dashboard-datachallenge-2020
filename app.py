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
import urllib

# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
app.title = 'Covid-19 Impact Dashboard'
server = app.server


#ACCESS S3
[AWSID] = '[AWSID]'
[YOUR AWS SECRET] = '[YOUR AWS SECRET]'
client = boto3.client('s3', aws_access_key_id=[AWSID], [YOUR AWS SECRET]_access_key=[YOUR AWS SECRET])
ABC = '[BUCKETNAME]'



## CORN PRICES
object_key = 'Corn Prices - 59 Year Historical Chart.csv'
csv_obj = client.get_object(Bucket=ABC, Key=object_key)
body = csv_obj['Body']
csv_string = body.read().decode('utf-8')
df_CornPrices = pd.read_csv(StringIO(csv_string))
## PROCESS
df_CornPrices.dropna(inplace=True)
df_CornPrices['date'] = pd.to_datetime(df_CornPrices['date'], utc=False, errors='coerce')
df_CornPrices.index = df_CornPrices['date']
df_CornPrices.drop(['date'], axis = 1, inplace= True)
y_CornPrices = df_CornPrices.resample('MS').mean()
y_CornPrices.fillna(y_CornPrices.bfill())
y_CornPrices = y_CornPrices['2015':]
y_CornPrices = pd.DataFrame(data=y_CornPrices.values, index=y_CornPrices.index, columns=["value"])
## CALCULATION
mod = sm.tsa.statespace.SARIMAX(y_CornPrices,
                            order=(0, 1, 1),
                            seasonal_order=(1, 1, 1, 12),
                            enforce_stationarity=False,
                            enforce_invertibility=False)
results_CornPrices = mod.fit()
pred_dynamic_CornPrices = results_CornPrices.get_prediction(start=pd.to_datetime('2020-01-01'), dynamic=True, full_results=True)
pred_dynamic_ci_CornPrices = pred_dynamic_CornPrices.conf_int()
## DEVELOP CHART 
figCornPrices = go.Figure()
figCornPrices.add_trace(go.Scatter(x=y_CornPrices.index, y=y_CornPrices["value"], mode='lines'))
figCornPrices.add_trace(go.Scatter(x=pred_dynamic_ci_CornPrices.index, y=pred_dynamic_CornPrices.predicted_mean.values, mode='lines'))
figCornPrices.add_shape(dict(type="line", x0=pd.to_datetime('2020-02-01'), y0=0, x1=pd.to_datetime('2020-02-01'), y1=pred_dynamic_ci_CornPrices.iloc[:, 1].values.max(), line=dict(color="Red", width=3  )))
figCornPrices.add_trace(go.Scatter(x=pred_dynamic_ci_CornPrices.index, y=pred_dynamic_ci_CornPrices.iloc[:, 0], fill='tonexty', mode='lines', line_color='#d4d3d2')) # fill down to xaxis
figCornPrices.add_trace(go.Scatter(x=pred_dynamic_ci_CornPrices.index, y=pred_dynamic_ci_CornPrices.iloc[:, 1], fill='tonexty', mode='lines', line_color='#d4d3d2')) # fill to trace0 y
figCornPrices.update_layout(showlegend=False)
figCornPrices.update_layout(yaxis_tickprefix = '$')
figCornPrices.update_layout(autosize=False, width=300, height=150, margin=dict(l=10, r=10, b=10, t=10, pad=1))
## GENERATE FILE FOR DOWNLOAD
csv_stringCornPrices = df_CornPrices.to_csv(index=True, encoding='utf-8')
csv_stringCornPrices = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_stringCornPrices)


## OIL PRICES
object_key = 'Crude Oil Prices: Daily Closing Values.csv'
csv_obj = client.get_object(Bucket=ABC, Key=object_key)
body = csv_obj['Body']
csv_string = body.read().decode('utf-8')
df_OilPrices = pd.read_csv(StringIO(csv_string))
#df_OilPrices = pd.read_csv('data/Crude Oil Prices_ Daily Closing Values.csv')
## PROCESS
df_OilPrices.dropna(inplace=True)
df_OilPrices['date'] = pd.to_datetime(df_OilPrices['date'], utc=False, errors='coerce')
df_OilPrices.index = df_OilPrices['date']
df_OilPrices.drop(['date'], axis = 1, inplace= True)
y_OilPrices = df_OilPrices.resample('MS').mean()
y_OilPrices.fillna(y_OilPrices.bfill())
y_OilPrices = y_OilPrices['2015':]
y_OilPrices = pd.DataFrame(data=y_OilPrices.values, index=y_OilPrices.index, columns=["price"])
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
figOilPrices.update_layout(yaxis_tickprefix = '$')
## GENERATE FILE FOR DOWNLOAD
csv_stringOilPrices = df_OilPrices.to_csv(index=True, encoding='utf-8')
csv_stringOilPrices = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_stringOilPrices)

## SOY PRICES
object_key = 'Soybean Prices - 45 Year Historical Chart.csv'
csv_obj = client.get_object(Bucket=ABC, Key=object_key)
body = csv_obj['Body']
csv_string = body.read().decode('utf-8')
df_SoyPrices = pd.read_csv(StringIO(csv_string))
## PROCESS
df_SoyPrices.dropna(inplace=True)
df_SoyPrices['date'] = pd.to_datetime(df_SoyPrices['date'], utc=False, errors='coerce')
df_SoyPrices.index = df_SoyPrices['date']
df_SoyPrices.drop(['date'], axis = 1, inplace= True)
y_SoyPrices = df_SoyPrices.resample('MS').mean()
y_SoyPrices.fillna(y_SoyPrices.bfill())
y_SoyPrices = y_SoyPrices['2015':]
y_SoyPrices = pd.DataFrame(data=y_SoyPrices.values, index=y_SoyPrices.index, columns=["price"])
## CALCULATION
mod = sm.tsa.statespace.SARIMAX(y_SoyPrices,
                            order=(0, 1, 1),
                            seasonal_order=(1, 1, 1, 12),
                            enforce_stationarity=False,
                            enforce_invertibility=False)
results_SoyPrices = mod.fit()
pred_dynamic_SoyPrices = results_SoyPrices.get_prediction(start=pd.to_datetime('2020-01-01'), dynamic=True, full_results=True)
pred_dynamic_ci_SoyPrices = pred_dynamic_SoyPrices.conf_int()
##DEVELOP CHART 
figSoyPrices = go.Figure()
figSoyPrices.add_trace(go.Scatter(x=y_SoyPrices.index, y=y_SoyPrices['price'], mode='lines'))
figSoyPrices.add_trace(go.Scatter(x=pred_dynamic_ci_SoyPrices.index, y=pred_dynamic_SoyPrices.predicted_mean.values, mode='lines'))
figSoyPrices.add_shape(dict(type="line", x0=pd.to_datetime('2020-02-01'), y0=0, x1=pd.to_datetime('2020-02-01'), y1=pred_dynamic_ci_SoyPrices.iloc[:, 1].values.max(), line=dict(color="Red", width=3  )))
figSoyPrices.add_trace(go.Scatter(x=pred_dynamic_ci_SoyPrices.index, y=pred_dynamic_ci_SoyPrices.iloc[:, 0], fill='tonexty', mode='lines', line_color='#d4d3d2')) # fill down to xaxis
figSoyPrices.add_trace(go.Scatter(x=pred_dynamic_ci_SoyPrices.index, y=pred_dynamic_ci_SoyPrices.iloc[:, 1], fill='tonexty', mode='lines', line_color='#d4d3d2')) # fill to trace0 y
figSoyPrices.update_layout(showlegend=False)
figSoyPrices.update_layout(autosize=False, width=300, height=150, margin=dict(l=10, r=10, b=10, t=10, pad=1))
figSoyPrices.update_layout(yaxis_tickprefix = '$')
## GENERATE FILE FOR DOWNLOAD
csv_stringSoyPrices = df_SoyPrices.to_csv(index=True, encoding='utf-8')
csv_stringSoyPrices = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_stringSoyPrices)


## RICE PRICES
object_key = 'CBOT Rough Rice Futures #1 (RR1).csv'
csv_obj = client.get_object(Bucket=ABC, Key=object_key)
body = csv_obj['Body']
csv_string = body.read().decode('utf-8')
df_RicePrices = pd.read_csv(StringIO(csv_string))
## PROCESS
df_RicePrices.dropna(inplace=True)
df_RicePrices['date'] = pd.to_datetime(df_RicePrices['date'], utc=False, errors='coerce')
df_RicePrices.index = df_RicePrices['date']
df_RicePrices.drop(['date'], axis = 1, inplace= True)
y_RicePrices = df_RicePrices.resample('MS').mean()
y_RicePrices.fillna(y_RicePrices.bfill())
y_RicePrices = y_RicePrices['2015':]
y_RicePrices = pd.DataFrame(data=y_RicePrices.values, index=y_RicePrices.index, columns=["price"])
## CALCULATION
mod = sm.tsa.statespace.SARIMAX(y_RicePrices,
                            order=(0, 1, 1),
                            seasonal_order=(1, 1, 1, 12),
                            enforce_stationarity=False,
                            enforce_invertibility=False)
results_RicePrices = mod.fit()
pred_dynamic_RicePrices = results_RicePrices.get_prediction(start=pd.to_datetime('2020-01-01'), dynamic=True, full_results=True)
pred_dynamic_ci_RicePrices = pred_dynamic_RicePrices.conf_int()
##DEVELOP CHART 
figRicePrices = go.Figure()
figRicePrices.add_trace(go.Scatter(x=y_RicePrices.index, y=y_RicePrices['price'], mode='lines'))
figRicePrices.add_trace(go.Scatter(x=pred_dynamic_ci_RicePrices.index, y=pred_dynamic_RicePrices.predicted_mean.values, mode='lines'))
figRicePrices.add_shape(dict(type="line", x0=pd.to_datetime('2020-02-01'), y0=0, x1=pd.to_datetime('2020-02-01'), y1=pred_dynamic_ci_RicePrices.iloc[:, 1].values.max(), line=dict(color="Red", width=3  )))
figRicePrices.add_trace(go.Scatter(x=pred_dynamic_ci_RicePrices.index, y=pred_dynamic_ci_RicePrices.iloc[:, 0], fill='tonexty', mode='lines', line_color='#d4d3d2')) # fill down to xaxis
figRicePrices.add_trace(go.Scatter(x=pred_dynamic_ci_RicePrices.index, y=pred_dynamic_ci_RicePrices.iloc[:, 1], fill='tonexty', mode='lines', line_color='#d4d3d2')) # fill to trace0 y
figRicePrices.update_layout(showlegend=False)
figRicePrices.update_layout(autosize=False, width=300, height=150, margin=dict(l=10, r=10, b=10, t=10, pad=1))
figRicePrices.update_layout(yaxis_tickprefix = '$')
## GENERATE FILE FOR DOWNLOAD
csv_stringRicePrices = df_RicePrices.to_csv(index=True, encoding='utf-8')
csv_stringRicePrices = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_stringRicePrices)


## BROILER PRODUCTION
object_key = 'SlaughterCounts-Broilers.csv'
csv_obj = client.get_object(Bucket=ABC, Key=object_key)
body = csv_obj['Body']
csv_string = body.read().decode('utf-8')
df_BroilerProd = pd.read_csv(StringIO(csv_string))
## PROCESS
df_BroilerProd.dropna(inplace=True)
df_BroilerProd['date'] = pd.to_datetime(df_BroilerProd['date'], utc=False, errors='coerce')
df_BroilerProd.index = df_BroilerProd['date']
df_BroilerProd.drop(['date'], axis = 1, inplace= True)
y_BroilerProd = df_BroilerProd.resample('MS').mean()
y_BroilerProd.fillna(y_BroilerProd.bfill())
y_BroilerProd = y_BroilerProd['2015':]
y_BroilerProd = pd.DataFrame(data=y_BroilerProd.values, index=y_BroilerProd.index, columns=["value"])
## CALCULATION
mod = sm.tsa.statespace.SARIMAX(y_BroilerProd,
                            order=(0, 1, 1),
                            seasonal_order=(1, 1, 1, 12),
                            enforce_stationarity=False,
                            enforce_invertibility=False)
results_BroilerProd = mod.fit()
pred_dynamic_BroilerProd = results_BroilerProd.get_prediction(start=pd.to_datetime('2020-01-01'), dynamic=True, full_results=True)
pred_dynamic_ci_BroilerProd = pred_dynamic_BroilerProd.conf_int()
##DEVELOP CHART 
figBroilerProd = go.Figure()
figBroilerProd.add_trace(go.Scatter(x=y_BroilerProd.index, y=y_BroilerProd['value'], mode='lines'))
figBroilerProd.add_trace(go.Scatter(x=pred_dynamic_ci_BroilerProd.index, y=pred_dynamic_BroilerProd.predicted_mean.values, mode='lines'))
figBroilerProd.add_shape(dict(type="line", x0=pd.to_datetime('2020-02-01'), y0=0, x1=pd.to_datetime('2020-02-01'), y1=pred_dynamic_ci_BroilerProd.iloc[:, 1].values.max(), line=dict(color="Red", width=3  )))
figBroilerProd.add_trace(go.Scatter(x=pred_dynamic_ci_BroilerProd.index, y=pred_dynamic_ci_BroilerProd.iloc[:, 0], fill='tonexty', mode='lines', line_color='#d4d3d2')) # fill down to xaxis
figBroilerProd.add_trace(go.Scatter(x=pred_dynamic_ci_BroilerProd.index, y=pred_dynamic_ci_BroilerProd.iloc[:, 1], fill='tonexty', mode='lines', line_color='#d4d3d2')) # fill to trace0 y
figBroilerProd.update_layout(showlegend=False)
figBroilerProd.update_layout(autosize=False, width=300, height=150, margin=dict(l=10, r=10, b=10, t=10, pad=1))
## GENERATE FILE FOR DOWNLOAD
csv_stringBroilerProd = df_BroilerProd.to_csv(index=True, encoding='utf-8')
csv_stringBroilerProd = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_stringBroilerProd)

## OTHER CHICKENS PRODUCTION
object_key = 'SlaughterCounts-Other chickens.csv'
csv_obj = client.get_object(Bucket=ABC, Key=object_key)
body = csv_obj['Body']
csv_string = body.read().decode('utf-8')
df_OtherChickProd = pd.read_csv(StringIO(csv_string))
## PROCESS
df_OtherChickProd.dropna(inplace=True)
df_OtherChickProd['date'] = pd.to_datetime(df_OtherChickProd['date'], utc=False, errors='coerce')
df_OtherChickProd.index = df_OtherChickProd['date']
df_OtherChickProd.drop(['date'], axis = 1, inplace= True)
y_OtherChickProd = df_OtherChickProd.resample('MS').mean()
y_OtherChickProd.fillna(y_OtherChickProd.bfill())
y_OtherChickProd = y_OtherChickProd['2015':]
y_OtherChickProd = pd.DataFrame(data=y_OtherChickProd.values, index=y_OtherChickProd.index, columns=["value"])
## CALCULATION
mod = sm.tsa.statespace.SARIMAX(y_OtherChickProd,
                            order=(0, 1, 1),
                            seasonal_order=(1, 1, 1, 12),
                            enforce_stationarity=False,
                            enforce_invertibility=False)
results_OtherChickProd = mod.fit()
pred_dynamic_OtherChickProd = results_OtherChickProd.get_prediction(start=pd.to_datetime('2020-01-01'), dynamic=True, full_results=True)
pred_dynamic_ci_OtherChickProd = pred_dynamic_OtherChickProd.conf_int()
##DEVELOP CHART 
figOtherChickProd = go.Figure()
figOtherChickProd.add_trace(go.Scatter(x=y_OtherChickProd.index, y=y_OtherChickProd['value'], mode='lines'))
figOtherChickProd.add_trace(go.Scatter(x=pred_dynamic_ci_OtherChickProd.index, y=pred_dynamic_OtherChickProd.predicted_mean.values, mode='lines'))
figOtherChickProd.add_shape(dict(type="line", x0=pd.to_datetime('2020-02-01'), y0=0, x1=pd.to_datetime('2020-02-01'), y1=pred_dynamic_ci_OtherChickProd.iloc[:, 1].values.max(), line=dict(color="Red", width=3  )))
figOtherChickProd.add_trace(go.Scatter(x=pred_dynamic_ci_OtherChickProd.index, y=pred_dynamic_ci_OtherChickProd.iloc[:, 0], fill='tonexty', mode='lines', line_color='#d4d3d2')) # fill down to xaxis
figOtherChickProd.add_trace(go.Scatter(x=pred_dynamic_ci_OtherChickProd.index, y=pred_dynamic_ci_OtherChickProd.iloc[:, 1], fill='tonexty', mode='lines', line_color='#d4d3d2')) # fill to trace0 y
figOtherChickProd.update_layout(showlegend=False)
figOtherChickProd.update_layout(autosize=False, width=300, height=150, margin=dict(l=10, r=10, b=10, t=10, pad=1))
## GENERATE FILE FOR DOWNLOAD
csv_stringOtherChickProd = df_OtherChickProd.to_csv(index=True, encoding='utf-8')
csv_stringOtherChickProd = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_stringOtherChickProd)


## TURKEY PRODUCTION
object_key = 'SlaughterCounts-Turkeys.csv'
csv_obj = client.get_object(Bucket=ABC, Key=object_key)
body = csv_obj['Body']
csv_string = body.read().decode('utf-8')
df_TurkeyProd = pd.read_csv(StringIO(csv_string))
## PROCESS
df_TurkeyProd.dropna(inplace=True)
df_TurkeyProd['date'] = pd.to_datetime(df_TurkeyProd['date'], utc=False, errors='coerce')
df_TurkeyProd.index = df_TurkeyProd['date']
df_TurkeyProd.drop(['date'], axis = 1, inplace= True)
y_TurkeyProd = df_TurkeyProd.resample('MS').mean()
y_TurkeyProd.fillna(y_TurkeyProd.bfill())
y_TurkeyProd = y_TurkeyProd['2015':]
y_TurkeyProd = pd.DataFrame(data=y_TurkeyProd.values, index=y_TurkeyProd.index, columns=["value"])
## CALCULATION
mod = sm.tsa.statespace.SARIMAX(y_TurkeyProd,
                            order=(0, 1, 1),
                            seasonal_order=(1, 1, 1, 12),
                            enforce_stationarity=False,
                            enforce_invertibility=False)
results_TurkeyProd = mod.fit()
pred_dynamic_TurkeyProd = results_TurkeyProd.get_prediction(start=pd.to_datetime('2020-01-01'), dynamic=True, full_results=True)
pred_dynamic_ci_TurkeyProd = pred_dynamic_TurkeyProd.conf_int()
##DEVELOP CHART 
figTurkeyProd = go.Figure()
figTurkeyProd.add_trace(go.Scatter(x=y_TurkeyProd.index, y=y_TurkeyProd['value'], mode='lines'))
figTurkeyProd.add_trace(go.Scatter(x=pred_dynamic_ci_TurkeyProd.index, y=pred_dynamic_TurkeyProd.predicted_mean.values, mode='lines'))
figTurkeyProd.add_shape(dict(type="line", x0=pd.to_datetime('2020-02-01'), y0=0, x1=pd.to_datetime('2020-02-01'), y1=pred_dynamic_ci_TurkeyProd.iloc[:, 1].values.max(), line=dict(color="Red", width=3  )))
figTurkeyProd.add_trace(go.Scatter(x=pred_dynamic_ci_TurkeyProd.index, y=pred_dynamic_ci_TurkeyProd.iloc[:, 0], fill='tonexty', mode='lines', line_color='#d4d3d2')) # fill down to xaxis
figTurkeyProd.add_trace(go.Scatter(x=pred_dynamic_ci_TurkeyProd.index, y=pred_dynamic_ci_TurkeyProd.iloc[:, 1], fill='tonexty', mode='lines', line_color='#d4d3d2')) # fill to trace0 y
figTurkeyProd.update_layout(showlegend=False)
figTurkeyProd.update_layout(autosize=False, width=300, height=150, margin=dict(l=10, r=10, b=10, t=10, pad=1))
## GENERATE FILE FOR DOWNLOAD
csv_stringTurkeyProd = df_TurkeyProd.to_csv(index=True, encoding='utf-8')
csv_stringTurkeyProd = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_stringTurkeyProd)


### STYLES
styleH2 = {'color':'##81473'}
styleH3S = {'color':'#a60f0f','text-decoration': 'underline'}
styleH3D = {'color':'#1124a6','text-decoration': 'underline'}
styleTitlesS = {'color':'red', 'font-size':'14px', 'font-weight' :'bold'}
styleTitlesD = {'color':'blue', 'font-size':'14px', 'font-weight' :'bold'}
styleDownload = {'color':'green', 'font-size':'10px'}

## LAYOUT DESIGN
app.layout = html.Div(className="body",
    children=[
        html.H2("COVID-19 IMPACT DASHBOARD [Proof of Concept]", style=styleH2), 
        html.Div(className="row",
        children=[
            html.Div(className="columnleft",
            children=[
                html.H3("Supply chain impact", style=styleH3S),
                html.Table(className="center",
                    children=[
                        html.Tr(
                            children=[
                                html.Td(
                                    children=[
                                        html.P("Oil Prices", style=styleTitlesS),
                                        dcc.Graph(figure=figOilPrices),
                                        html.A('[Download csv]',id='download-Oil',download="Oil Prices.csv",href=csv_stringOilPrices,target="_blank", style=styleDownload)
                                    ]
                                ),
                                html.Td(
                                    children=[
                                        html.P("Corn Prices", style=styleTitlesS),
                                        dcc.Graph(figure=figCornPrices),
                                        html.A('[Download csv]',id='download-Corn',download="Corn Prices.csv",href=csv_stringCornPrices,target="_blank", style=styleDownload)
                                    ]
                                )
                            ]
                        ),
                        html.Tr(
                            children=[
                                html.Td(
                                    children=[
                                        html.P("Soy bean prices", style=styleTitlesS),
                                        dcc.Graph(figure=figSoyPrices),
                                        html.A('[Download csv]',id='download-Soy',download="Soy Prices.csv",href=csv_stringSoyPrices,target="_blank", style=styleDownload)
                                    ]
                                ),
                                html.Td(
                                    children=[
                                        html.P("Rice prices", style=styleTitlesS),
                                        dcc.Graph(figure=figRicePrices),
                                        html.A('[Download csv]',id='download-Rice',download="Rice Prices.csv",href=csv_stringRicePrices,target="_blank", style=styleDownload)
                                    ]
                                )
                            ]                            
                        )
                    ]
                )
            ]),
            html.Div(className="columnright",
            children=[
                html.H3("US Production output impact", style=styleH3D),
                html.Table(className="center",
                    children=[
                        html.Tr(
                            children=[
                                html.Td(
                                    children=[
                                        html.P("Broiler production", style=styleTitlesD),
                                        dcc.Graph(figure=figBroilerProd),
                                        html.A('[Download csv]',id='download-Broiler',download="Broiler Production.csv",href=csv_stringBroilerProd,target="_blank", style=styleDownload)
                                    ]
                                ),
                                html.Td(
                                    children=[
                                        html.P("Other chicken production", style=styleTitlesD),
                                        dcc.Graph(figure=figOtherChickProd),
                                        html.A('[Download csv]',id='download-OtherChick',download="Other Chick Production.csv",href=csv_stringOtherChickProd,target="_blank", style=styleDownload)
                                    ]
                                )
                            ]
                        ),
                        html.Tr(
                            children=[
                                html.Td(
                                    children=[
                                        html.P("Turkey production", style=styleTitlesD),
                                        dcc.Graph(figure=figTurkeyProd),
                                        html.A('[Download csv]',id='download-Turkey',download="Turkey Production.csv",href=csv_stringTurkeyProd,target="_blank", style=styleDownload)
                                    ]
                                ),
                                html.Td(
                                    children=[
                                        html.P(" ")
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
