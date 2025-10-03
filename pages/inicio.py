import dash
from dash import html, dcc
import numpy as np
import plotly.graph_objects as go

p_0 = 100
r = 0.3

t = np.linspace(0, 100, num=200)
P = p_0*np.exp(r*t)

trace = go.Scatter(
    x=t,
    y=P,
    mode="lines+markers",
    # color="red"
    line=dict(
        dash='dot',
        color='black'
    ),
    marker=dict(
        symbol="square",
        size=2
    ),
    # name="P(t)=P_0*e^{rt}",
    hovertemplate="t=%{x}<br> P=%{y}"
)

fig = go.Figure(data=trace)

fig.update_layout(
    title=dict(
        text="<b>Crecimiento de la población</b>",
        font=dict(
            size=20,
            color="red"
        ),
        x=0.5,
        y=.93
    ),
    xaxis_title="Tiempo",
    yaxis_title="Poblacion",
    margin=dict(l=40, r=20, t=20, b=10),
    paper_bgcolor="lightblue",
    plot_bgcolor="white",
    font=dict(
        family="Outfit",
        size=11,
        color="black"
    )
)

fig.update_xaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor="lightpink",
    zeroline=True,
    zerolinewidth=2,
    zerolinecolor="red"
)

fig.update_yaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor="lightpink",
    zeroline=True,
    zerolinewidth=2,
    zerolinecolor="red"
)

dash.register_page(__name__, path="/", name="inicio")

layout = html.Div(children=[
    html.H1("Bienvenido al inicio"),
    dcc.Markdown(
        """
        texto de prueba $\\alpha$
        """
    , mathjax=True),
    dcc.Graph(
        figure=fig,
        style={"height": "400px", "width":"100%"},
    )
])#falta corregir acá esto