import random
import numpy as np

from scipy.stats import poisson, binom
import plotly.graph_objs as go


def poisson_graph(mean):
    x = list(range(mean*3))
    x_label = [str(int(v)) for v in x]
    return go.Figure(
        data=[
            go.Bar(
                x=x_label,
                y=list(poisson.pmf(i, mean) for i in x),
                opacity=0.5)
        ]
    )


def binomial_graph(n, p):
    n = int(n)
    p = min(p, 1)

    x = range(n+2)
    x_label = [str(v) for v in x]
    return go.Figure(
        data=[
            go.Bar(
                x=x_label,
                y=list(binom.pmf(i, n, p) for i in x),
                opacity=0.5)
        ]
    )


def simple_random_walk(inventory, demand, orders, shipped, n=2, init=10, seed=0):
    np.random.seed(seed)
    x = list(range(100))
    steps = np.random.randint(-n, n+1, 99)
    y = [init]
    for step in steps:
        y.append(max(y[-1]+step, 0))
    inventory = go.Scatter(
        x=x,
        y=y,
        mode='lines+markers',
        name="'Inventory'",
        #hoverinfo='name',
        line=dict(shape='hv')
    )
    deltas = go.Scatter(
        x=x[0:-1],
        y=steps,
        mode='lines+markers',
        name="'Delta'",
        #hoverinfo='name',
        line=dict(shape='hv')
    )

    layout = dict(
        legend=dict(
            font=dict(
                size=16
            )
        )
    )
    print(inventory)
    return go.Figure(
        data=[inventory, deltas]
        #layout=layout
    )
