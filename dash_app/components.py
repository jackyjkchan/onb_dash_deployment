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
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum id lectus at ligula ultrices fringilla. Praesent in dignissim lacus. Fusce iaculis arcu semper convallis finibus. Pellentesque et cursus sem. Nulla auctor, nunc in interdum sagittis, eros tellus suscipit sem, sit amet tempor purus orci sed sapien. Donec eu lectus sit amet leo venenatis vulputate. Ut blandit ligula lorem, sed mollis tellus congue ac. Donec eu commodo ex, sed tempor massa. Nam nec fringilla mi.
    """),
    dbc.Row([
        dbc.Col([
            html.Label(children='''min_weekday_usage:'''),
            html.A(" "),
            dcc.Input(
                id='min_weekday_usage',
                type="number",
                value=1,
                min=0
            )
        ], width=4),
        dbc.Col([
            html.Label(children='''mode_weekday_usage:'''),
            html.A(" "),
            dcc.Input(
                id='mode_weekday_usage',
                value=1,
                type="number"
            )
        ], width=4),
        dbc.Col([
            html.Label(children='''max_weekday_usage:'''),
            html.A(" "),
            dcc.Input(
                id='max_weekday_usage',
                value=2,
                type="number"
            )
        ], width=4)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label(children='''min_weekend_usage:'''),
            html.A(" "),
            dcc.Input(
                id='min_weekend_usage',
                value=1,
                type="number",
                min=0
            )
        ], width=4),
        dbc.Col([
            html.Label(children='''mode_weekend_usage:'''),
            html.A(" "),
            dcc.Input(
                id='mode_weekend_usage',
                value=1,
                type="number"
            )
        ], width=4),
        dbc.Col([
            html.Label(children='''max_weekend_usage:'''),
            html.A(" "),
            dcc.Input(
                id='max_weekend_usage',
                value=2,
                type="number"
            )
        ], width=4)
    ])
]

ordering_policy_setup = [
    html.H3(id='policy_show', children='Ordering Policy Inputs'),
    html.P("""
Fusce posuere condimentum tristique. Pellentesque ex sapien, imperdiet sit amet est ac, ullamcorper posuere neque. Pellentesque rhoncus semper sapien nec egestas. Ut non egestas lorem. Aliquam erat volutpat. Cras tristique luctus erat, vel ultricies felis tincidunt sit amet. Vestibulum pretium, ligula nec aliquet hendrerit, felis felis convallis turpis, sed gravida leo libero nec purus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Vestibulum eleifend turpis elit, ut dignissim magna consectetur eu. Fusce sit amet ligula ullamcorper, mollis neque sit amet, tempus neque.
    """),
    dbc.Row([
        dbc.Col([
            html.Label(children='''max_level:'''),
            html.A(" "),
            dcc.Input(
                id='order_max_level',
                value=1,
                type="number"
            )
        ], width=4),
        dbc.Col([
            html.Label(children='''min_level:'''),
            html.A(" "),
            dcc.Input(
                id='order_min_level',
                value=1,
                type="number"
            )
        ], width=4),
        dbc.Col([
            html.Label(children='''frequency'''),
            html.A(" "),
            dcc.Input(
                id='frequency',
                value=2,
                type="number",
                min=1,
                step=1
            )
        ], width=4)
    ])
]

ordering_lead_time_setup = [
    html.H3(id='lead_time_show', children='Ordering Lead Time Inputs'),
    html.P("""
Mauris in purus consectetur, semper nunc eu, bibendum arcu. Nunc viverra nec nunc ac malesuada. Morbi vitae blandit justo. Nunc eget convallis velit. Nullam pretium lorem id mi pellentesque, aliquet euismod lacus posuere. Sed non purus interdum, fringilla lacus a, auctor massa. In quis blandit leo.
    """),
    dbc.Row([
        dbc.Col([
            html.Label(children='''min_lt:'''),
            html.A(" "),
            dcc.Input(
                id='min_lt',
                value=1,
                type="number",
                step=1
            )
        ], width=4),
        dbc.Col([
            html.Label(children='''mode_lt:'''),
            html.A(" "),
            dcc.Input(
                id='mode_lt',
                value=1,
                type="number",
                step=1
            )
        ], width=4),
        dbc.Col([
            html.Label(children='''max_lt:'''),
            html.A(" "),
            dcc.Input(
                id='max_lt',
                value=2,
                type="number",
                min=1,
                step=1
            )
        ], width=4)
    ])
]

initial_conditions = [
    html.H3(id='initialization_show', n_clicks=0, children='Initialization Settings'),
    html.P("""
Sed commodo in mi id ornare. Sed feugiat erat in urna malesuada ultrices. Nulla sit amet metus et diam euismod condimentum varius quis urna. In id mauris a nibh porttitor volutpat ac sit amet purus. Nulla facilisi. Nam consequat ultricies metus, vitae consectetur ligula condimentum non. Donec tincidunt justo nec diam venenatis euismod ac porta felis. Vestibulum euismod, elit laoreet volutpat feugiat, ex nisi pretium est, vel aliquet ipsum metus lobortis ligula. In venenatis, dui quis fringilla pulvinar, ante nibh pretium urna, ac commodo diam elit faucibus arcu. Proin volutpat mollis egestas. Ut efficitur aliquam neque et posuere. Sed facilisis enim metus, vitae hendrerit purus vehicula in.
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
Vivamus venenatis lectus at lacus vehicula, a porta nisi pretium. Maecenas a faucibus turpis, a tincidunt orci. Vestibulum laoreet dui sit amet sem blandit sodales. Donec auctor tempus metus, iaculis tincidunt purus varius ut. Vivamus sapien justo, iaculis sed sapien non, iaculis rutrum mauris. Fusce ut ligula sed orci tristique lacinia sit amet non leo. Nulla facilisi. Proin nisi ex, tincidunt vel lectus vitae, lacinia scelerisque est. Duis ornare eros vel venenatis laoreet. Sed posuere risus non congue auctor. Maecenas est urna, laoreet quis tristique nec, rutrum in tellus. Nunc viverra molestie nisi, pulvinar mollis elit tempus eget. Morbi vel felis rhoncus, iaculis lacus id, convallis augue.
    """),
    dbc.Row([
        dbc.Col([
            html.Label(children='''Simulation Lenth:'''),
            html.A(" "),
            dcc.Input(
                id='sim_length',
                value=100,
                type="number",
                min=30,
                max=1000,
                step=10
            )
        ], width=4),
        dbc.Col([
            html.Label(children='''Repetitions:'''),
            html.A(" "),
            dcc.Input(
                id='reps',
                value=10,
                type="number",
                min=10,
                max=1000,
                step=10
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
