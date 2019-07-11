import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

demand_histogram = [dcc.Graph(id='demand_histogram')]


weekday_usage_setup = [
    html.Button(id='item_demand_show', n_clicks=0, children='Item Demand Inputs'),
    html.Div(id="item_demand_components", children=[
        dbc.Row([
            dbc.Col([
                html.Div(children='''min_weekday_usage'''),
                dcc.Input(
                    id='min_weekday_usage',
                    value=1,
                    type="number",
                    min=0
                )
            ]),
            dbc.Col([
                html.Div(children='''mode_weekday_usage'''),
                dcc.Input(
                    id='mode_weekday_usage',
                    value=1,
                    type="number"
                )
            ]),
            dbc.Col([
                html.Div(children='''max_weekday_usage'''),
                dcc.Input(
                    id='max_weekday_usage',
                    value=1,
                    type="number"
                )
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Div(children='''min_weekend_usage'''),
                dcc.Input(
                    id='min_weekend_usage',
                    value=1,
                    type="number",
                    min=0
                )
            ]),
            dbc.Col([
                html.Div(children='''mode_weekend_usage'''),
                dcc.Input(
                    id='mode_weekend_usage',
                    value=1,
                    type="number"
                )
            ]),
            dbc.Col([
                html.Div(children='''max_weekend_usage'''),
                dcc.Input(
                    id='max_weekend_usage',
                    value=1,
                    type="number"
                )
            ])
        ])
    ])
]

run_button = [
    html.Div(children=[
        html.Button(id='run_button', n_clicks=0, children='Run')
    ])
]

simulation_outputs = [
    html.Div(children='Results'),
    dcc.Graph(id='inventory_trace')
]
