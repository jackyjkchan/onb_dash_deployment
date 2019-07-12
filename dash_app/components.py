import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

demand_histogram = [dcc.Graph(id='demand_histogram')]

weekday_usage_setup = [
    dbc.Button(id='item_demand_show', n_clicks=0, children='Item Demand Inputs'),
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
                    value=2,
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
                    value=2,
                    type="number"
                )
            ])
        ])
    ])
]

ordering_policy_setup = [
    dbc.Button(id='policy_show', n_clicks=0, children='Ordering Policy Inputs'),
    html.Div(id="policy_components", children=[
        html.Div(children='''max_level'''),
        dcc.Input(
            id='order_max_level',
            value=1,
            type="number"
        ),
        html.Div(children='''min_level'''),
        dcc.Input(
            id='order_min_level',
            value=1,
            type="number"
        ),
        html.Div(children='''frequency'''),
        dcc.Input(
            id='frequency',
            value=2,
            type="number",
            min=1,
            step=1
        )
    ])
]

ordering_lead_time_setup = [
    html.Button(id='lead_time_show', n_clicks=0, children='Ordering Lead Time Inputs'),
    html.Div(id="lead_time_components", children=[
        html.Div(children='''min_lt'''),
        dcc.Input(
            id='min_lt',
            value=1,
            type="number",
            step=1
        ),
        html.Div(children='''mode_lt'''),
        dcc.Input(
            id='mode_lt',
            value=1,
            type="number",
            step=1
        ),
        html.Div(children='''max_lt'''),
        dcc.Input(
            id='max_lt',
            value=2,
            type="number",
            min=1,
            step=1
        )
    ])
]

initial_conditions = [
    html.Button(id='initialization_show', n_clicks=0, children='Initialization Settings'),
    html.Div(id="initialization_components", children=[
        html.Div(children='''Initial Inventory Level'''),
        dcc.Input(
            id='initial_inventory',
            value=1,
            type="number",
            step=1
        ),
        html.Div(children='''Initial Outstanding Orders'''),
        dcc.Input(
            id='initial_orders',
            value=0,
            type="number",
            step=1
        )
    ])
]

simulation_settings = [
    html.Button(id='simulation_settings_show', n_clicks=0, children='Simulation Settings'),
    html.Div(id="simulation_settings_components", children=[
        html.Div(children='''Simulation Lenth'''),
        dcc.Input(
            id='sim_length',
            value=100,
            type="number",
            min=30,
            max=1000,
            step=10
        ),
        html.Div(children='''Repetitions'''),
        dcc.Input(
            id='reps',
            value=10,
            type="number",
            min=10,
            max=1000,
            step=1
        )
    ])
]

work_in_progress_dialog = dcc.ConfirmDialog(id='wip_dialog',
                                            message='Sorry, this feature is currently unavailable.')

run_button = [
    html.Div(children=[
        html.Button(id='run_button', n_clicks=0, children='Run')
    ])
]

simulation_outputs = [
    html.Div(children='Results'),
    dash_table.DataTable(id='table'),
    html.Div(children=[
        dcc.Graph(id='inventory_trace')],
        style={'display': 'inline-block', 'width': '100%', 'height': '100%'}
    )
]
