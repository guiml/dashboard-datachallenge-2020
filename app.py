import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
app.title = 'Displacement visualization tool'
server = app.server


### STYLES
LeftText = {'margin-left':'25px','margin-right':'25px', 'color':'whitesmoke', 'font-size':'12px', 'text-align': 'justify', 'text-justify': 'inter-word'}
LeftTextY = {'margin-left':'15px','margin-right':'25px', 'color':'purple', 'font-size':'14px', 'text-align': 'justify', 'text-justify': 'inter-word', 'font-weight' :'bold'}
LeftTextSmall = {'margin-left':'15px','margin-right':'25px', 'color':'purple', 'font-size':'10px', 'text-align': 'justify', 'text-justify': 'inter-word'}
CenterText = {'color':'whitesmoke', 'font-size':'12px'}
CenterTextLink = {'color':'rgb(253, 255, 136)', 'font-size':'12px'}
LeftTitle = {'color':'whitesmoke','text-decoration': 'underline'}


### DOWNLOADS

## APPLICATION START

## LAYOUT DESIGN
app.layout = html.Div(className="row",
    children=[
        html.Div(className='column left',
            children=[html.P('Redhook')])])


## CALLBACKS (to update the charts)

if __name__ == '__main__':
    app.run_server(debug=False)