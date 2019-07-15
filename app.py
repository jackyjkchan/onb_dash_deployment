import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

import dash_bootstrap_components as dbc
import dash_app.components as components
import dash_app.graphs as graphs
import dash_app.model as model

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        dbc.Container([
            html.H1("Supply Chain Simulation"),
            components.work_in_progress_dialog,
            html.Div(id="settings", children=[
                dbc.Row(dbc.Col([*components.weekday_usage_setup])),
                dbc.Row(dbc.Col([*components.ordering_policy_setup])),
                dbc.Row(dbc.Col([*components.ordering_lead_time_setup])),
                dbc.Row(dbc.Col([*components.initial_conditions])),
                dbc.Row(dbc.Col([*components.simulation_settings]))
            ]),
            *components.run_button,
            *components.simulation_outputs
        ], fluid=True)
    ])


@app.callback([Output('settings', 'style'),
               Output('show_hide_settings', 'children')],
              [Input('show_hide_settings', 'n_clicks')])
def item_demand_show(n_clicks):
    return ({'display': 'none'}, "Show") if n_clicks % 2 else ({'display': 'block'}, "Hide")


@app.callback(
    [Output(component_id='mode_weekday_usage', component_property='min'),
     Output(component_id='mode_weekday_usage', component_property='value')],
    [Input(component_id='min_weekday_usage', component_property='value')])
def weekday_usage_mode_constraint(min_weekday_usage):
    return min_weekday_usage, min_weekday_usage


@app.callback(
    [Output(component_id='max_weekday_usage', component_property='min'),
     Output(component_id='max_weekday_usage', component_property='value')],
    [Input(component_id='mode_weekday_usage', component_property='value')])
def weekday_usage_max_constraint(mode_weekday_usage):
    return mode_weekday_usage, mode_weekday_usage + 1


@app.callback(
    [Output(component_id='mode_weekend_usage', component_property='min'),
     Output(component_id='mode_weekend_usage', component_property='value')],
    [Input(component_id='min_weekend_usage', component_property='value')])
def weekend_usage_mode_constraint(min_weekend_usage):
    return min_weekend_usage, min_weekend_usage


# @app.callback(Output('policy_components', 'style'),
#               [Input('policy_show', 'n_clicks')])
# def item_demand_show(n_clicks):
#     return {'display': 'block'} if n_clicks % 2 else {'display': 'none'}


@app.callback(
    [Output(component_id='max_weekend_usage', component_property='min'),
     Output(component_id='max_weekend_usage', component_property='value')],
    [Input(component_id='mode_weekend_usage', component_property='value')])
def weekend_usage_max_constraint(mode_weekend_usage):
    return mode_weekend_usage, mode_weekend_usage + 1


@app.callback(
    [Output(component_id='order_min_level', component_property='max'),
     Output(component_id='order_min_level', component_property='value')],
    [Input(component_id='order_max_level', component_property='value')],
    [State(component_id='order_min_level', component_property='value')])
def order_min_constraint(order_max_level, order_min_level):
    value = order_max_level if order_min_level > order_max_level else order_min_level
    return order_max_level, value


# @app.callback(Output('lead_time_components', 'style'),
#               [Input('lead_time_show', 'n_clicks')])
# def lead_time_show(n_clicks):
#     return {'display': 'block'} if n_clicks % 2 else {'display': 'none'}


@app.callback(
    [Output(component_id='mode_lt', component_property='min'),
     Output(component_id='mode_lt', component_property='value')],
    [Input(component_id='min_lt', component_property='value')])
def weekday_usage_mode_constraint(min_lt):
    return min_lt, min_lt


@app.callback(
    [Output(component_id='max_lt', component_property='min'),
     Output(component_id='max_lt', component_property='value')],
    [Input(component_id='mode_lt', component_property='value')])
def weekday_usage_max_constraint(mode_lt):
    return mode_lt, mode_lt + 1


# @app.callback(Output('initialization_components', 'style'),
#               [Input('initialization_show', 'n_clicks')])
# def lead_time_show(n_clicks):
#     return {'display': 'block'} if n_clicks % 2 else {'display': 'none'}


@app.callback(Output('wip_dialog', 'displayed'),
              [Input('initial_orders', 'value')])
def display_confirm(value):
    if value:
        return True
    return False


# @app.callback(Output('simulation_settings_components', 'style'),
#               [Input('simulation_settings_show', 'n_clicks')])
# def sim_settings_show(n_clicks):
#     return {'display': 'block'} if n_clicks % 2 else {'display': 'none'}


@app.callback(
    [Output(component_id='inventory_trace', component_property='figure'),
     Output(component_id='table', component_property='columns'),
     Output(component_id='table', component_property='data')],
    [Input(component_id='run_button', component_property='n_clicks')],
    [State(component_id='min_weekday_usage', component_property='value'),
     State(component_id='mode_weekday_usage', component_property='value'),
     State(component_id='max_weekday_usage', component_property='value'),
     State(component_id='min_weekend_usage', component_property='value'),
     State(component_id='mode_weekend_usage', component_property='value'),
     State(component_id='max_weekend_usage', component_property='value'),
     State(component_id='order_max_level', component_property='value'),
     State(component_id='order_min_level', component_property='value'),
     State(component_id='frequency', component_property='value'),
     State(component_id='min_lt', component_property='value'),
     State(component_id='mode_lt', component_property='value'),
     State(component_id='max_lt', component_property='value'),
     State(component_id="initial_inventory", component_property='value'),
     State(component_id="sim_length", component_property='value'),
     State(component_id="reps", component_property='value')])
def run_model(run,
              min_weekday_usage, mode_weekday_usage, max_weekday_usage,
              min_weekend_usage, mode_weekend_usage, max_weekend_usage,
              order_max_level, order_min_level, frequency,
              min_lt, mode_lt, max_lt,
              initial_inventory,
              sim_length, reps):
    args = {
        "min_weekday_usage": min_weekday_usage,
        "mode_weekday_usage": mode_weekday_usage,
        "max_weekday_usage": max_weekday_usage,
        "min_weekend_usage": min_weekend_usage,
        "mode_weekend_usage": mode_weekend_usage,
        "max_weekend_usage": max_weekend_usage,
        "max_level": order_max_level,
        "min_level": order_min_level,
        "frequency": frequency,
        "min_lt": min_lt,
        "mode_lt": mode_lt,
        "max_lt": max_lt,
        "num_reps": 10,
        "current_inventory_level": initial_inventory,
        "RunLength": sim_length,
        "num_reps": reps
    }

    fig, df = model.run(args) if run else ({}, pd.DataFrame())
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict('records')
    return fig, columns, data


if __name__ == '__main__':
    app.run_server(debug=True)
