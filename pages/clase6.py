import dash 
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import odeint

dash.register_page(__name__, path="/clase6", name="Modelo SIR")

layout = html.Div([
    html.Div([
        html.H2("Modelo SIR - Epidemiologia", className="title"),
        html.Div([
            html.Label("Población Total N= "),
            dcc.Input(id="input-n", type = "number", value = 1000, className="input-field")
        ]),
        html.Div([
            html.Label("Tasa de transmisión (r)= "),
            dcc.Input(id="input-b", type = "number", value = 0.3, step=0.01, className="input-field")
        ]),
        html.Div([
            html.Label("Tasa de recuperación (g) = "),
            dcc.Input(id="input-g", type = "number", value = 0.1, step=0.1, className="input-field")
        ]),
        html.Div([
            html.Label("Infectados iniciales (I)= "),
            dcc.Input(id="input-I0", type = "number", value = 1, className="input-field")
        ]),
        html.Div([
            html.Label("Tiempo de simulación: "),
            dcc.Input(id="input-tiempo", type = "number", value = 100, className="input-field")
        ]),
        
        html.Button("Generar campo", id = "btn-generar"),
        
        #Ejemplos
        # html.Div([
        #     html.H3("Ejemplos para probar:"),
        #     html.P("dx/dt=x, dy/dt=y"),
        #     html.P("dx/dt=-x, dy/dt=y"),
        #     html.P("dx/dt=-y, dy/dt=np.cos(x)"),
        # ])
    ], className="contain-left"),
    html.Div([
        html.H2("Evolución de la epidemia", className="title"),
        dcc.Graph(id="grafica-sir", style={"height":"450px","width":"100%"}),
        #html.Div(id="info-campo")
    ], className="contain-right")
], className="page-container")
def modelo_sir(y, t, b, g, N):
    S,I,R = y 

    dS_dt = -b*S*I/N
    dI_dt = b*S*I/N-g*I
    dR_dt = g*I

    return [dS_dt, dI_dt, dR_dt]


@callback(
    Output("grafica-sir", "figure")
     #Output("info-campo", "children")
     ,
     Input("btn-generar", "n_clicks"),
     State("input-n", "value"),
     State("input-b", "value"),
     State("input-g", "value"),
     State("input-I0", "value"),
     State("input-tiempo", "value"),
    prevent_initial_call=False
    )
def simular_sir(n_clicks, n, beta, gamma, I0, tiempo_max):
    S0 = n-I0 
    R0_inicial = 0
    y0 = [S0, I0, R0_inicial]
    t = np.linspace(0, tiempo_max, 200)
    try:
        solucion = odeint(modelo_sir, y0, t, args=(beta, gamma, n))
        S, I, R = solucion.T
    except Exception as e:
        S = np.full_like(t, S0)
        I = np.full_like(t, I0)
        R = np.full_like(t, R0_inicial)
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=S,
        mode = 'lines',
        name = 'Suceptibles (S)',
        line = dict(color='blue', width=2),
        hovertemplate = "Día: %{x:.0f} <br> Suceptibles :%{y:.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=t, y=I,
        mode = 'lines',
        name='Infectados(I)',
        line = dict(color='red', width=2),
        hovertemplate = "Día: %{x:.0f} <br> Infectados :%{y:.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=t, y=R,
        mode = 'lines',
        name='Recuperados (R)',
        line = dict(color='green', width=2),
        hovertemplate = "Día: %{x:.0f} <br> Recuperados :%{y:.0f}<extra></extra>"
    ))

    fig.update_layout(
        title=dict(
            text = f"<b>Evolucion del modelo SIR</b>",
            x=0.5, font=dict(size=16, color='darkblue')
        ),
        xaxis_title = "Tiempo (días)",
        yaxis_title="Número de personas",
        paper_bgcolor="lightcyan",
        plot_bgcolor="white",
        legend=dict(
            orientation='h', yanchor='bottom',y=1.02,
            xanchor='right', x=.5
        )
    )
    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor = "lightpink",
        zeroline=True, zerolinewidth=2, zerolinecolor="red",
        showline=True, linecolor="black", linewidth=2, mirror=True,
    )
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor = "lightpink",
        zeroline=True, zerolinewidth=2, zerolinecolor="red",
        showline=True, linecolor="black", linewidth=2, mirror=True,
    )

    return fig

# def generar_campo(n_clicks, fx_str, fy_str, xmax, ymax, n):
#     x=np.linspace(-xmax,xmax, n )
#     y = np.linspace(-ymax,ymax,n)
#     X,Y = np.meshgrid(x,y)
#     info_mensaje = ""
#     try:
#         diccionario = {
#             "x":X,
#             "y":Y,
#             "np":np,
#             "sin":np.sin,
#             "cos":np.cos,
#             "tan":np.tan,
#             "exp":np.exp,
#             'sqrt':np.sqrt,
#             'pi':np.pi,
#             'e':np.e 
#         }
#         fx = eval(fx_str, {}, diccionario)
#         fy = eval(fy_str, {}, diccionario)
#         mag_max = np.max(np.sqrt(fx**2+fy**2))
#         mag_min = np.min(np.sqrt(fx**2+fy**2))
#         info_mensaje = f"Magnitud: min ={mag_min:.2f}, max = {mag_max:.2f}"
#     except Exception as error: 
#         fx = np.zeros_like(X)
#         fy = np.zeros_like(Y)
#         info_mensaje = f"Error en las expresiones {str(error)}"
    
#     fig = go.Figure()

#     for i in range(n):
#         for j in range(n):
#             x0,y0=X[i,j], Y[i,j]
#             x1,y1 = x0+fx[i,j],y0+fy[i,j]
#             fig.add_trace(go.Scatter(
#                 x = [x0,x1],
#                 y = [y0,y1],
#                 mode = "lines+markers",
#                 line = dict(color="blue", width=2),
#                 showlegend=False 
#             ))
#     fig.update_layout(
#         title=dict(
#             text = f"<b>Campo Vectorial:dx/dt = {fx_str}, dy/dt = {fy_str}",
#             x=0.5
#         ),
#         xaxis_title = "x",
#         yaxis_title="y",
#         paper_bgcolor="lightyellow",
#         plot_bgcolor="white",
        
#     )
#     fig.update_xaxes(
#         showgrid=True, gridwidth=1, gridcolor = "lightpink",
#         zeroline=True, zerolinewidth=2, zerolinecolor="red",
#         showline=True, linecolor="black", linewidth=2, mirror=True,
#         range=[-xmax*1.1,xmax*1.1]
#     )
#     fig.update_yaxes(
#         showgrid=True, gridwidth=1, gridcolor = "lightpink",
#         zeroline=True, zerolinewidth=2, zerolinecolor="red",
#         showline=True, linecolor="black", linewidth=2, mirror=True,
#         range=[-ymax*1.1,ymax*1.1])
#     return fig, info_mensaje