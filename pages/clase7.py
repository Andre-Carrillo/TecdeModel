import dash 
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import odeint

dash.register_page(__name__, path="/clase7", name="Modelo SEIR")

layout = html.Div([
    html.Div([
        html.H2("Modelo SEIR - Epidemiología", className="title"),
        html.Div([
            html.Label("Población Total N = "),
            dcc.Input(id="input-n-2", type="number", value=1000, className="input-field")
        ]),
        html.Div([
            html.Label("Tasa de transmisión (β) = "),
            dcc.Input(id="input-b-2", type="number", value=0.3, step=0.01, className="input-field")
        ]),
        html.Div([
            html.Label("Tasa de incubación (σ) = "),
            dcc.Input(id="input-s", type="number", value=0.2, step=0.01, className="input-field")
        ]),
        html.Div([
            html.Label("Tasa de recuperación (γ) = "),
            dcc.Input(id="input-g", type="number", value=0.1, step=0.01, className="input-field")
        ]),
        html.Div([
            html.Label("Expuestos iniciales (E₀) = "),
            dcc.Input(id="input-E0", type="number", value=0, className="input-field")
        ]),
        html.Div([
            html.Label("Infectados iniciales (I₀) = "),
            dcc.Input(id="input-I0-2", type="number", value=1, className="input-field")
        ]),
        html.Div([
            html.Label("Tiempo de simulación (días) = "),
            dcc.Input(id="input-tiempo-2", type="number", value=160, className="input-field")
        ]),
        
        html.Button("Simular modelo", id="btn-generar"),
    ], className="contain-left"),
    
    html.Div([
        html.H2("Evolución de la epidemia", className="title"),
        dcc.Graph(id="grafica-seir", style={"height":"450px", "width":"100%"}),
    ], className="contain-right")
], className="page-container")


# --- Modelo SEIR ---
def modelo_seir(y, t, beta, sigma, gamma, N):
    S, E, I, R = y
    dS_dt = -beta * S * I / N
    dE_dt = beta * S * I / N - sigma * E
    dI_dt = sigma * E - gamma * I
    dR_dt = gamma * I
    return [dS_dt, dE_dt, dI_dt, dR_dt]


# --- Callback principal ---
@callback(
    Output("grafica-seir", "figure"),
    Input("btn-generar", "n_clicks"),
    State("input-n-2", "value"),
    State("input-b-2", "value"),
    State("input-s", "value"),
    State("input-g", "value"),
    State("input-E0", "value"),
    State("input-I0-2", "value"),
    State("input-tiempo-2", "value"),
    prevent_initial_call=False
)
def simular_seir(n_clicks, N, beta, sigma, gamma, E0, I0, tiempo_max):
    S0 = N - E0 - I0
    R0_inicial = 0
    y0 = [S0, E0, I0, R0_inicial]
    t = np.linspace(0, tiempo_max, 300)

    try:
        solucion = odeint(modelo_seir, y0, t, args=(beta, sigma, gamma, N))
        S, E, I, R = solucion.T
    except Exception as e:
        S = np.full_like(t, S0)
        E = np.full_like(t, E0)
        I = np.full_like(t, I0)
        R = np.full_like(t, R0_inicial)

    # --- Gráfica ---
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=S,
        mode='lines', name='Susceptibles (S)',
        line=dict(color='blue', width=2),
        hovertemplate="Día: %{x:.0f}<br>Susceptibles: %{y:.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=t, y=E,
        mode='lines', name='Expuestos (E)',
        line=dict(color='orange', width=2),
        hovertemplate="Día: %{x:.0f}<br>Expuestos: %{y:.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=t, y=I,
        mode='lines', name='Infectados (I)',
        line=dict(color='red', width=2),
        hovertemplate="Día: %{x:.0f}<br>Infectados: %{y:.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=t, y=R,
        mode='lines', name='Recuperados (R)',
        line=dict(color='green', width=2),
        hovertemplate="Día: %{x:.0f}<br>Recuperados: %{y:.0f}<extra></extra>"
    ))

    fig.update_layout(
        title=dict(
            text=f"<b>Evolución del modelo SEIR</b>",
            x=0.5, font=dict(size=16, color='darkblue')
        ),
        xaxis_title="Tiempo (días)",
        yaxis_title="Número de personas",
        paper_bgcolor="lightcyan",
        plot_bgcolor="white",
        legend=dict(
            orientation='h', yanchor='bottom', y=1.02,
            xanchor='right', x=.5
        )
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="lightpink",
                     zeroline=True, zerolinewidth=2, zerolinecolor="red",
                     showline=True, linecolor="black", linewidth=2, mirror=True)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="lightpink",
                     zeroline=True, zerolinewidth=2, zerolinecolor="red",
                     showline=True, linecolor="black", linewidth=2, mirror=True)

    return fig
