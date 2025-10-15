import dash
from dash import html, dcc, Input, Output, callback
import plotly.graph_objects as go
from models.logistic_model import logistic_with_harvest  

dash.register_page(__name__, path="/clase4", name="Clase 4")

layout = html.Div(
    children=[
        # html.H2("Técnicas de Modelamiento Matemático", style={"textAlign": "center", "color": "white", "backgroundColor": "#0033cc", "padding": "10px"}),

        html.Div([
            html.Div([
                html.H4("Parámetros del modelo", style={"textAlign": "center"}),

                html.Label("Población inicial P(0):"),
                dcc.Input(id="p0", type="number", value=200, style={"width": "100%", "marginBottom": "10px"}),

                html.Label("Tasa de crecimiento (r):"),
                dcc.Input(id="r", type="number", value=0.04, step=0.01, style={"width": "100%", "marginBottom": "10px"}),

                html.Label("Capacidad de carga (K):"),
                dcc.Input(id="K", type="number", value=750, style={"width": "100%", "marginBottom": "10px"}),

                html.Label("Tiempo máximo (t):"),
                dcc.Input(id="tmax", type="number", value=100, style={"width": "100%", "marginBottom": "10px"}),

                html.Label("Cosecha (h):"),
                dcc.Input(id="h", type="number", value=30, style={"width": "100%", "marginBottom": "10px"}),

                # html.Button("Generar gráfica", id="btn-generar2", n_clicks=1,
                #             style={"width": "100%", "backgroundColor": "#0033cc", "color": "white", "padding": "10px", "border": "none", "cursor": "pointer", "marginTop": "10px"}),

            ], style={"flex": "1", "padding": "20px", "backgroundColor": "white", "borderRadius": "8px", "marginRight": "20px"}),

            html.Div([
                html.H4("Gráfica", style={"textAlign": "center"}),
                dcc.Graph(id="grafica-retardo", style={"height": "400px"})
            ], style={"flex": "2", "padding": "20px", "backgroundColor": "#e8f0ff", "borderRadius": "8px"})
        ], style={"display": "flex", "justifyContent": "center", "alignItems": "stretch", "padding": "20px"})
    ],
    style={"fontFamily": "Outfit", "backgroundColor": "#f5f6fa", "minHeight": "100vh"}
)


@callback(
    Output("grafica-retardo", "figure"),
    # Input("btn-generar2", "n_clicks"),
    Input("p0", "value"),
    Input("r", "value"),
    Input("K", "value"),
    Input("tmax", "value"),
    Input("h", "value"),
)
def actualizar_grafica(p0, r, K, tmax, h):
    if not all([p0, r, K, tmax]):
        return go.Figure()

    t, P = logistic_with_harvest(p0, r, K, tmax, h=h)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t, y=P,
        mode="lines+markers",
        name="P(t)",
        line=dict(color="blue", width=2),
        marker=dict(size=3),
        hovertemplate="t=%{x}<br>P=%{y:.2f}"
    ))

    fig.add_hline(y=K, line=dict(color="red", dash="dot"), annotation_text="K", annotation_position="top right")

    fig.update_layout(
        title="<b>Crecimiento logístico con cosecha</b>",
        xaxis_title="Tiempo (t)",
        yaxis_title="Población P(t)",
        plot_bgcolor="white",
        paper_bgcolor="#e8f0ff",
        font=dict(family="Outfit", size=12),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    fig.update_xaxes(gridcolor="lightgray", zeroline=True, zerolinecolor="red")
    fig.update_yaxes(gridcolor="lightgray", zeroline=True, zerolinecolor="red")

    return fig
