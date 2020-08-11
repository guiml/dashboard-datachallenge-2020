# NYU CUSP 2020 - CEQR Capstone project Visualization Tool

## General description (scope)

The purpose of this file is to create a tool to visualize the results of the models developed to support our capstone project. This is a complimentary tool built using the results generated by the [Digital CEQR 2.0](https://github.com/akash-y/CUSP_CEQR)

## Execution

To execute this dashboard I recommend to have Anaconda installed. 

1) Download the files to a local folder
2) Create a Python virtual environment
3) Activate Python virtual environment
4) Execute pip install -r requirements.txt
5) Execute python app.py
6) Copy the URL address shown (ex: http://127.0.0.1:8050/)
7) Open the URL (ex: http://127.0.0.1:8050/) on browser

## Files structure:

* /data | Inputs folder
* /assets | Images and style sheet
* app.py | The main application code
* requirements.txt | Library requirements needed to run the application  
* Procfile, setup.py and runtime.txt | Dash required files for running the application
## References used to build this application:

- https://www.datacamp.com/community/tutorials/learn-build-dash-python
- https://www.statworx.com/at/blog/how-to-build-a-dashboard-in-python-plotly-dash-step-by-step-tutorial/
- https://github.com/STATWORX/blog/blob/master/DashApp/app_basic.py
- https://docs.mapbox.com/help/tutorials/choropleth-studio-gl-pt-1/
- https://studio.mapbox.com/tilesets/

Besides that I had inumerous visits to https://stackoverflow.com/ , https://www.geeksforgeeks.org/ , https://pandas.pydata.org/ , https://dash.plotly.com/ , among others sites used as reference.