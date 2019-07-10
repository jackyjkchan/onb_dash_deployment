import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import dash_app.components as components
import dash_app.graphs as graphs
import dash_app.model as model

app = dash.Dash('example')

app.layout = html.Div([
    *components.weekday_usage_setup,
    *components.run_button,
    *components.simulation_outputs
])


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
    Output(component_id='inventory_trace', component_property='figure'),
    [Input(component_id='run_button', component_property='n_clicks')],
    [State(component_id='min_weekday_usage', component_property='value'),
     State(component_id='mode_weekday_usage', component_property='value'),
     State(component_id='max_weekday_usage', component_property='value')])
def run_model(run, min_weekday_usage, mode_weekday_usage, max_weekday_usage):
    args = {
        "min_weekday_usage": min_weekday_usage,
        "mode_weekday_usage": mode_weekday_usage,
        "max_weekday_usage": max_weekday_usage,
        "num_reps": 10
    }
    fig = model.run(args) if run else {}
    return fig


#
# @app.callback(
#    Output(component_id='set_poisson_mean', component_property='style'),
#    [Input(component_id='demand_selection', component_property='value')])
# def show_poisson_inputs(selection):
#     return {'display': 'block'} if selection == 'poisson' else {'display': 'none'}
#
#
# @app.callback(
#    [Output(component_id='set_binomial_n', component_property='style'),
#     Output(component_id='set_binomial_p', component_property='style')],
#    [Input(component_id='demand_selection', component_property='value')])
# def show_nb_inputs(selection):
#     on = [{'display': 'block'}]*2
#     off = [{'display': 'none'}]*2
#     return on if selection == 'binomial' else off
#
#
# @app.callback(
#    Output(component_id='demand_histogram', component_property='figure'),
#    [Input(component_id='demand_selection', component_property='value'),
#     Input(component_id='set_poisson_mean', component_property='value'),
#     Input(component_id='set_binomial_n', component_property='value'),
#     Input(component_id='set_binomial_p', component_property='value')])
# def show_demand_histogram(family, poisson_mean, binom_n, binom_p):
#     if family == "poisson":
#         r = graphs.poisson_graph(poisson_mean)
#         return graphs.poisson_graph(poisson_mean)
#     elif family == "binomial":
#         return graphs.binomial_graph(binom_n, binom_p)
#     else:
#         return graphs.binomial_graph(binom_n, binom_p)


if __name__ == '__main__':
    app.run_server(debug=True)
