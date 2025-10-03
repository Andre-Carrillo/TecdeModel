import dash
from dash import html, dcc
import numpy as np
import plotly.graph_objects as go


dash.register_page(__name__, path="/clase2", name="Clase 2")



p_0 = 50
r = 0.1
k=200

t = np.linspace(0, 60, num=500)
P = k*p_0*np.exp(r*t)/(k+p_0*np.exp(r*t)-1)

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

layout = html.Div(children=[
    html.H1("Crecimiento Logístico", style={"text-align":"center"}),
    html.Div(children=[dcc.Markdown(
        """

        Para modelar el crecimiento de la población considerando recursos limitados, se puede usar el **crecimiento logístico**.  

        La variable $t$ representa el tiempo, y $P(t)$ es la población en función del tiempo. La ecuación diferencial que describe el crecimiento logístico es:  

        $$$
        \\frac{dP}{dt} = r P \\left(1 - \\frac{P}{K}\\right),
        $$$    

        donde $r>0$ es la tasa de crecimiento y $K>0$ es la **capacidad de carga**, es decir, el máximo número de individuos que el entorno puede sostener.  

        La solución de esta ecuación diferencial se conoce como **curva logística**:  

        $$$
        P(t) = \\frac{K}{1 + \\left(\\frac{K - P_0}{P_0}\\right)e^{-r t}},
        $$$

        donde $P_0$ es la población inicial. Esta función describe un crecimiento rápido al inicio, que luego se desacelera a medida que la población se acerca a $K$.  

        **Ejemplo:**  
        Supongamos que $P_0 = 50$, $r = 0.1$ y $K = 200$. Entonces la población en función del tiempo es:  

        $$$
        P(t) = \\frac{200}{1 + \\left(\\frac{200 - 50}{50}\\right)e^{-0.1 t}} = \\frac{200}{1 + 3 e^{-0.1 t}}.
        $$$

        En este caso, la población crece rápidamente al inicio y se estabiliza cerca de $200$ cuando $t$ es grande.
        """
    , mathjax=True, style={"flex":1}, className="card"),
    dcc.Graph(
        figure=fig,
        style={"height": "400px", "width":"100%", "flex":1},
        className="card"
    )], style={"display":"flex"})
])#falta corregir acá esto