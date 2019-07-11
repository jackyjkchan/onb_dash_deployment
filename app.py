import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import dash_bootstrap_components as dbc
import dash_app.components as components
import dash_app.graphs as graphs
import dash_app.model as model

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.GRID])

app.layout = html.Div([
    *components.weekday_usage_setup,
    *components.run_button,
    *components.simulation_outputs
])


@app.callback(Output('item_demand_components', 'style'),
              [Input('item_demand_show', 'n_clicks')])
def item_demand_show(n_clicks):
    if n_clicks % 2:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


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
    return mode_weekday_usage, mode_weekday_usage


@app.callback(
    [Output(component_id='mode_weekend_usage', component_property='min'),
     Output(component_id='mode_weekend_usage', component_property='value')],
    [Input(component_id='min_weekend_usage', component_property='value')])
def weekend_usage_mode_constraint(min_weekend_usage):
    return min_weekend_usage, min_weekend_usage


@app.callback(
    [Output(component_id='max_weekend_usage', component_property='min'),
     Output(component_id='max_weekend_usage', component_property='value')],
    [Input(component_id='mode_weekend_usage', component_property='value')])
def weekend_usage_max_constraint(mode_weekend_usage):
    return mode_weekend_usage, mode_weekend_usage


@app.callback(
    Output(component_id='inventory_trace', component_property='figure'),
    [Input(component_id='run_button', component_property='n_clicks')],
    [State(component_id='min_weekday_usage', component_property='value'),
     State(component_id='mode_weekday_usage', component_property='value'),
     State(component_id='max_weekday_usage', component_property='value'),
     State(component_id='min_weekend_usage', component_property='value'),
     State(component_id='mode_weekend_usage', component_property='value'),
     State(component_id='max_weekend_usage', component_property='value')
     ])
def run_model(run,
              min_weekday_usage, mode_weekday_usage, max_weekday_usage,
              min_weekend_usage, mode_weekend_usage, max_weekend_usage):
    args = {
        "min_weekday_usage": min_weekday_usage,
        "mode_weekday_usage": mode_weekday_usage,
        "max_weekday_usage": max_weekday_usage,
        "min_weekend_usage": min_weekend_usage,
        "mode_weekend_usage": mode_weekend_usage,
        "max_weekend_usage": max_weekend_usage,
        "num_reps": 10
    }
    fig = model.run(args) if run else {}
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
