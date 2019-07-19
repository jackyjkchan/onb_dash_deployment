import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

demand_histogram = [dcc.Graph(id='demand_histogram')]

weekday_usage_setup = [
    html.H3(id='item_demand_show', children='Item Demand Inputs'),
    html.P("""
    What is the minimum, most frequent, and maximum number of items used on a typical weekday? What is the minimum, 
    most frequent, and maximum number of items used on a typical Saturday or Sunday? Weekend usage values are inputted 
    separately from the weekday usage values to allow for a reduction in surgery that generally occur on weekends. 
    However, if the usage of an item is consistent across all days of the week, the weekend usage values should equal 
    the weekday values.
    """),
    dbc.Row([
        dbc.Col([
            html.Label(children='''Max Weekday Usage:'''),
            html.A(" "),
            dcc.Input(
                id='max_weekday_usage',
                type="number",
                value=1,
                min=1,
            )
        ], width=4),
        dbc.Col([
            html.Label(children='''Mode Weekday Usage:'''),
            html.A(" "),
            dcc.Input(
                id='mode_weekday_usage',
                value=0,
                type="number"
            )
        ], width=4),
        dbc.Col([
            html.Label(children='''Min Weekday Usage:'''),
            html.A(" "),
            dcc.Input(
                id='min_weekday_usage',
                value=0,
                type="number"
            )
        ], width=4)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label(children='''Max Weekend Usage:'''),
            html.A(" "),
            dcc.Input(
                id='max_weekend_usage',
                value=1,
                type="number",
                min=0
            )
        ], width=4),
        dbc.Col([
            html.Label(children='''Mode Weekend Usage:'''),
            html.A(" "),
            dcc.Input(
                id='mode_weekend_usage',
                value=0,
                type="number"
            )
        ], width=4),
        dbc.Col([
            html.Label(children='''Min Weekday Usage:'''),
            html.A(" "),
            dcc.Input(
                id='min_weekend_usage',
                value=0,
                type="number"
            )
        ], width=4)
    ])
]

ordering_policy_setup = [
    html.H3(id='policy_show', children='Ordering Policy Inputs'),
    html.P("""
    Frequency of Review: How many business days are there between each review of the inventory level? 
    This parameter can be toggled to test different frequencies of review, while the default value is 1 day 
    representing review every business day.
    """),
    html.P("""
    Reorder Point: After a review of the inventory is conducted, the inventory level is compared to the reorder point. 
    If the inventory level in the core drops down to at or below the reorder point, then an order is placed.
    """),
    html.P("""
    Order Up to Point: After it is determined that an order must be placed, the amount of inventory to be ordered has 
    to be determined. A common way that hospitals determine the order quantity is by using an order up to point to 
    represent the number of items the hospital should have on hand and on route.
    """),
    dbc.Row([
        dbc.Col([
            html.Label(children='''Order Up to Point:'''),
            html.A(" "),
            dcc.Input(
                id='order_max_level',
                value=1,
                type="number",
                min=1
            )
        ], width=3),
        dbc.Col([
            html.Label(children='''Reorder Point:'''),
            html.A(" "),
            dcc.Input(
                id='order_min_level',
                value=0,
                type="number"
            )
        ], width=3),
        dbc.Col([
            html.Label(children='''Frequency:'''),
            html.A(" "),
            dcc.Input(
                id='frequency',
                value=2,
                type="number",
                min=1,
                step=1
            )
        ], width=3),
        dbc.Col([
            html.Label(children='''unit_of_measure'''),
            html.A(" "),
            dcc.Input(
                id='unit_of_measure',
                value=2,
                type="number",
                min=1,
                step=1
            )
        ], width=3)
    ])
]

ordering_lead_time_setup = [
    html.H3(id='lead_time_show', children='Ordering Lead Time Inputs'),
    html.P("""
    What is the minimum, most frequent, and maximum number of business days between when an order is placed and the order 
    arrives and is unpacked into the inventory core?
    """),
    dbc.Row([
        dbc.Col([
            html.Label(children='''Max Lead Time:'''),
            html.A(" "),
            dcc.Input(
                id='max_lt',
                value=1,
                type="number",
                step=1
            )
        ], width=4),
        dbc.Col([
            html.Label(children='''Mode Lead Time:'''),
            html.A(" "),
            dcc.Input(
                id='mode_lt',
                value=0,
                type="number",
                step=1
            )
        ], width=4),
        dbc.Col([
            html.Label(children='''Min Lead Time:'''),
            html.A(" "),
            dcc.Input(
                id='min_lt',
                type="number",
                value=0,
                step=1
            )
        ], width=4)
    ])
]

initial_conditions = [
    html.H3(id='initialization_show', n_clicks=0, children='Initialization Settings'),
    html.P("""
    Current Inventory Level: How many items are currently in the inventory core?
    """),
    dbc.Row([
        dbc.Col([
            html.Label(children='''Initial Inventory Level:'''),
            html.A(" "),
            dcc.Input(
                id='initial_inventory',
                value=1,
                type="number",
                step=1
            )
        ], width=4),
        dbc.Col([
            html.Label(children='''Initial Outstanding Orders:'''),
            html.A(" "),
            dcc.Input(
                id='initial_orders',
                value=0,
                type="number",
                step=1
            )
        ], width=4)
    ])
]

simulation_settings = [
    html.H3(id='simulation_settings_show', children='Simulation Settings'),
    html.P("""
    Forecast Horizon: How many days into the future should the inventory policy be simulated for?
    """),
    html.P("""
    Replications: How many times to run this simulation in parallel for averaging results over?
    """),
    dbc.Row([
        dbc.Col([
            html.Label(children='''Forecast Horizon:'''),
            html.A(" "),
            dcc.Input(
                id='sim_length',
                value=100,
                type="number",
                min=1,
                max=1000,
            )
        ], width=4),
        dbc.Col([
            html.Label(children='''Replications:'''),
            html.A(" "),
            dcc.Input(
                id='reps',
                value=10,
                type="number",
                min=1,
                max=1000
            )
        ], width=4)
    ])
]

work_in_progress_dialog = dcc.ConfirmDialog(id='wip_dialog',
                                            message='Sorry, this feature is currently unavailable.')

run_button = [
    html.Div(children=[
        html.Button(id='show_hide_settings', n_clicks=0, children='Show/Hide Settings')
    ]),
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
