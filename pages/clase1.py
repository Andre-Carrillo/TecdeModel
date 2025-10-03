import dash
from dash import html, dcc
import numpy as np
import plotly.graph_objects as go


dash.register_page(__name__, path="/clase1", name="Clase 1")


p_0 = 100
r = 0.03

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

dash.register_page(__name__, path="/1", name="Clase 1")

layout = html.Div(children=[
    html.H1("Crecimiento Exponencial", style={"text-align":"center"}),
    html.Div(children=[dcc.Markdown(
        """
        Para modelar el crecimiento de la población mediante una ecuación diferencial,
        primero tenemos que introducir algunas variables y términos relevantes. 
        La variable $t$ representará el tiempo. Las unidades de tiempo pueden ser horas,
        días, semanas, meses o incluso años. Cualquier problema dado debe especificar 
        las unidades utilizadas en ese problema en particular. La variable $P$
        representará a la población. Como la población varía con el tiempo que es una función
        del tiempo. Por lo tanto, utilizamos la notación $P(t)$ para la población
        en función del tiempo. Si $P(t)$ es una función diferenciable, entonces la primera
        derivada $\\dfrac{dP}{dt}$ representa la tasa insantanea de cambio ide la población
        en función del tiempo.
        Un ejemplo de función de crecimiento exponencial es $P(t)=P_0e^{rt}$. En esta
        función, $P(t)$ representa la población en el momento $t$, $P_0$ representa la
        población inicial (población en el tiempo $t=0$), y la constante $r>0$ se denomina
        tasa de crecimiento. Aquí $P_0=100$ y $r=0.03$.

        """
    , mathjax=True, style={"flex":1}, className="card"),
    dcc.Graph(
        figure=fig,
        style={"height": "400px", "width":"100%", "flex":1},
        className="card"
    )], style={"display":"flex"})
])#falta corregir acá esto