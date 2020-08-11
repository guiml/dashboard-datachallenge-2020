import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from matplotlib import pyplot
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import base64
import itertools
import warnings
import io


# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
app.title = ' tool'
server = app.server


### STYLES
LeftText = {'margin-left':'25px','margin-right':'25px', 'color':'whitesmoke', 'font-size':'12px', 'text-align': 'justify', 'text-justify': 'inter-word'}
LeftTextY = {'margin-left':'15px','margin-right':'25px', 'color':'purple', 'font-size':'14px', 'text-align': 'justify', 'text-justify': 'inter-word', 'font-weight' :'bold'}
LeftTextSmall = {'margin-left':'15px','margin-right':'25px', 'color':'purple', 'font-size':'10px', 'text-align': 'justify', 'text-justify': 'inter-word'}
CenterText = {'color':'whitesmoke', 'font-size':'12px'}
CenterTextLink = {'color':'rgb(253, 255, 136)', 'font-size':'12px'}
LeftTitle = {'color':'whitesmoke','text-decoration': 'underline'}


### DOWNLOADS
Oil = pd.read_csv('data/Crude Oil Prices_ Daily Closing Values.csv')
Broiler = pd.read_csv('data/SlaughterCounts-Broilers.csv')


###APP
df_OilPrices = pd.read_csv('data/Crude Oil Prices_ Daily Closing Values.csv')
df_OilPrices.dropna(inplace=True)
df_OilPrices['date'] = pd.to_datetime(df_OilPrices['date'], utc=False)
df_OilPrices.index = df_OilPrices['date']
df_OilPrices.drop(['date'], axis = 1, inplace= True)
y_OilPrices = df_OilPrices.resample('MS').mean()
y_OilPrices.fillna(y_OilPrices.bfill())
y_OilPrices = y_OilPrices['2015':]
mod = sm.tsa.statespace.SARIMAX(y_OilPrices,
                            order=(0, 1, 1),
                            seasonal_order=(1, 1, 1, 12),
                            enforce_stationarity=False,
                            enforce_invertibility=False)
results_OilPrices = mod.fit()
pred_dynamic_OilPrices = results_OilPrices.get_prediction(start=pd.to_datetime('2020-01-01'), dynamic=True, full_results=True)
pred_dynamic_ci_OilPrices = pred_dynamic_OilPrices.conf_int()


OilPrices = px.line(df_OilPrices, x=df_OilPrices.index, y=df_OilPrices['price'])

OilPrices.update_layout({'height': 200, 'width': 400})




## APPLICATION START

## LAYOUT DESIGN
app.layout = html.Div(
    children=[dcc.Graph(figure=OilPrices)])



if __name__ == '__main__':
    app.run_server(debug=True)

