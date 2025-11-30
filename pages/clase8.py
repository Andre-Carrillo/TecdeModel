import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import requests # Librería necesaria para llamadas API
import pandas as pd

dash.register_page(__name__, path="/clase8", name="Datos API (Clima)")

layout = html.Div([
    html.Div([
        html.H2("Consumo de API", className="title"),
        html.P("Consulta de datos históricos de temperatura usando Open-Meteo API.", style={'color': 'gray', 'fontSize': '14px'}),
        
        # Inputs para la API
        html.Div([
            html.Label("Latitud:"),
            dcc.Input(id="input-lat", type="number", value=-12.0464, className="input-field", step=0.01) # Default Lima
        ]),
        html.Div([
            html.Label("Longitud:"),
            dcc.Input(id="input-lon", type="number", value=-77.0428, className="input-field", step=0.01)
        ]),
        html.Div([
            html.Label("Días pasados a consultar:"),
            dcc.Input(id="input-days", type="number", value=7, min=1, max=90, className="input-field")
        ]),
        
        html.Br(),
        html.Button("Obtener Datos", id="btn-api-call"),
        
        # Explicación didáctica
        html.Div([
            html.H3("¿Cómo funciona?"),
            html.P("Al hacer clic, Python envía una solicitud HTTP a una URL externa, recibe un JSON, procesa los datos y actualiza la gráfica."),
            html.A("Ver documentación de API", href="https://open-meteo.com/", target="_blank")
        ], style={'marginTop': '20px', 'borderTop': '1px solid #ccc', 'paddingTop': '10px'})

    ], className="contain-left"),

    html.Div([
        html.H2("Visualización de Datos Externos", className="title"),
        dcc.Graph(id="grafica-api", style={"height":"450px","width":"100%"}),
        html.Div(id="info-api", style={'marginTop': '10px', 'fontWeight': 'bold'})
    ], className="contain-right")

], className="page-container")

@callback(
    [Output("grafica-api", "figure"),
     Output("info-api", "children")],
    Input("btn-api-call", "n_clicks"),
    State("input-lat", "value"),
    State("input-lon", "value"),
    State("input-days", "value"),
    prevent_initial_call=False
)
def consultar_api_clima(n_clicks, lat, lon, days):
    # Valores por defecto para la primera carga si n_clicks es None
    if lat is None: lat = -12.04
    if lon is None: lon = -77.04
    if days is None: days = 3

    info_mensaje = "Esperando consulta..."
    fig = go.Figure()

    # URL de la API (Open Meteo es gratuita y no requiere Key)
    # Pedimos temperatura horaria de los ultimos 'days' días
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&past_days={days}&hourly=temperature_2m&forecast_days=1"

    try:
        # 1. Realizar la llamada a la API
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # 2. Procesar los datos (El JSON tiene una estructura específica)
            # data['hourly']['time'] es una lista de fechas
            # data['hourly']['temperature_2m'] es una lista de temperaturas
            times = data['hourly']['time']
            temps = data['hourly']['temperature_2m']
            
            # Estadísticas simples
            temp_max = max(temps)
            temp_min = min(temps)
            temp_avg = sum(temps) / len(temps)
            
            info_mensaje = f"Temp Máx: {temp_max}°C | Temp Mín: {temp_min}°C | Promedio: {temp_avg:.2f}°C"

            # 3. Crear la gráfica
            fig.add_trace(go.Scatter(
                x=times,
                y=temps,
                mode="lines",
                name="Temperatura",
                line=dict(color="#ff7f50", width=3),
                fill='tozeroy' # Relleno debajo de la linea
            ))

            fig.update_layout(
                title=dict(
                    text=f"<b>Temperatura en Lat:{lat}, Lon:{lon}</b>",
                    x=0.5
                ),
                xaxis_title="Tiempo",
                yaxis_title="Temperatura (°C)",
                paper_bgcolor="lightyellow",
                plot_bgcolor="white",
                hovermode="x unified"
            )
            
            fig.update_xaxes(
                showgrid=True, gridwidth=1, gridcolor="lightgray",
                showline=True, linecolor="black"
            )
            fig.update_yaxes(
                showgrid=True, gridwidth=1, gridcolor="lightgray",
                showline=True, linecolor="black"
            )

        else:
            info_mensaje = f"Error en la API: Código {response.status_code}"

    except Exception as e:
        info_mensaje = f"Error de conexión o procesamiento: {str(e)}"
        # Gráfica vacía en caso de error
        fig.update_layout(
            paper_bgcolor="lightyellow",
            plot_bgcolor="white"
        )

    return fig, info_mensaje