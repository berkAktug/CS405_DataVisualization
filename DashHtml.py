import dash
import dash_core_components as dcc
import dash_html_components as html

from datetime import datetime as dt

from textwrap import dedent as d

from Common import locationList #, locationDataframe, locationDictionary
from Common import min_date, max_date
# EXTERNAL STYLESHEET
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = html.Div([

    html.Div(children=[

        html.Div( 
            className="div-for-dropdown",
            children=[
                # Dropdown for locations on map
                dcc.Dropdown(
                    id="location_dropdown",
                    options=[ {"label": i, "value": i} for i in locationList ],
                    placeholder="Select a location",
                ),
                dcc.DatePickerSingle(
                    id="date-picker",
                    min_date_allowed=dt(min_date.year, min_date.month, min_date.day),
                    max_date_allowed=dt(max_date.year, max_date.month, max_date.day),
                    initial_visible_month=dt(min_date.year, min_date.month, min_date.day),
                    date=dt(min_date.year, min_date.month, min_date.day).date(),
                    display_format="MMMM D, YYYY",
                    style={"border": "0px solid black"},
                ),
                dcc.Dropdown(
                    id="bar-selector",
                    options=[
                        {
                            "label": str(n) + ":00",
                            "value": str(n),
                        }
                        for n in range(24)
                    ],
                    multi=True,
                    placeholder="Select certain hours",
                )
            ],
        ),
    ]),

    html.Div(className='row', children=[
        dcc.Graph( id = "taxi_map"),

        html.Div([
            dcc.Markdown(d("""
                Click on the map to see details here!.
            """)),
            html.Pre(id='map_click-data', style=styles['pre']),
        ], className='three columns'),

        html.Div([
            dcc.Markdown(d("""
                Select points on the map to see details here!
            """)),
            html.Pre(id='map_selected-data', style=styles['pre']),
        ], className='three columns'),

        html.Div([
            dcc.Markdown(d("""
                Zooming values are being represented here!
            """)),
            html.Pre(id='map_relayout-data', style=styles['pre']),
        ], className='three columns')
    ]),

    html.Div(className='row', children=[
        dcc.Graph(id='passanger_chart'),

        html.Div([
            dcc.Markdown(d("""
                Hover on data from Passanger Count Graph to see here!
            """)),
            html.Pre(id='hover-data', style=styles['pre'])
        ], className='three columns'),

        html.Div([
            dcc.Markdown(d("""
                Click on data from Passanger Count Graph to see here!
            """)),
            html.Pre(id='click-data', style=styles['pre']),
        ], className='three columns'),

        html.Div([
            dcc.Markdown(d("""
                Select Data from Passanger Count Graph to see here!
            """)),
            html.Pre(id='selected-data', style=styles['pre']),
        ], className='three columns'),
    ]),

    html.Div(className='row', children=[
        dcc.Graph(id="passanger_cash_chart"),

        html.Div([
            dcc.Markdown(d("""
                Hover on data from Cash Count (per hour) Graph to see here!
            """)),
            html.Pre(id='cash_hover-data', style=styles['pre'])
        ], className='three columns'),

        html.Div([
            dcc.Markdown(d("""
                Click on data from Cash Count (per hour) Graph to see here!
            """)),
            html.Pre(id='cash_click-data', style=styles['pre']),
        ], className='three columns'),

        html.Div([
            dcc.Markdown(d("""
                Select Data from Cash Count (per hour) Graph to see here!
            """)),
            html.Pre(id='cash_selected-data', style=styles['pre']),
        ], className='three columns'),
    ]),
])
