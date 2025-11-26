import dash
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import odeint 


dash.register_page(__name__, path="/aplicaciones", name="Aplicaciones")


# --- 2. Definición del Layout ---
layout = html.Div(className='content-container', children=[
    
    # Usamos un 'card' de ancho completo, igual que tu página de 'inicio.py'
    html.Div(className='card', style={'width': '100%'}, children=[
        
        html.H1("Aplicaciones y Generalización del Modelo SIR"),
        
        dcc.Markdown(r"""
            Como hemos visto en los modelos SIR y SEIR, el sistema básico de Ecuaciones
            Diferenciales puede modelar la propagación de una enfermedad.
            
            Sin embargo, el concepto de "contagio" es más general. El mismo modelo
            matemático puede usarse para describir cualquier proceso donde una "idea"
            o "estado" se transfiere por contacto en una población cerrada.
            
            A continuación, se presentan 3 estudios de caso basados en las asignaciones
            del curso, que demuestran la flexibilidad del modelo.
        """, mathjax=True),
        
        html.Hr(),

        # --- 3. Pestañas (Tabs) para comparar los 3 casos ---
        dcc.Tabs(id='tabs-sir-aplicaciones', value='tab-1', children=[
            
            # --- PESTAÑA 1: EPIDEMIA ---
            dcc.Tab(label='Caso 1: Epidemia (Enfermedad)', value='tab-1', children=[
                html.Div(className='tab-content', children=[
                    html.H3("Escenario: Brote de Enfermedad"),
                    dcc.Markdown(r"""
                        * **S (Susceptibles):** Estudiantes sanos.
                        * **I (Infectados):** Estudiantes enfermos que contagian.
                        * **R (Recuperados):** Estudiantes inmunes.
                    """),
                    
                    html.H4("Parámetros del Caso"),
                    dcc.Markdown(r"""
                        * $N = 7138$
                        * $S_0 = 7137$, $I_0 = 1$, $R_0 = 0$
                        * $\beta = 1 / 7138$
                        * $k = 0.40$
                        * **$R_0$ (Num. Reproductivo): $\approx 2.5$**
                    """, mathjax=True),
                    
                   # html.Img(src=dash.get_asset_url('simulacion_a1.png')),
                    html.Div([
                        html.H2("Evolución de la epidemia", className="title"),
                        dcc.Graph(id="grafica-sir-2", style={"height":"450px","width":"100%"}),
                        #html.Div(id="info-campo")
                        ], className="contain-right"),

    html.Div([
        html.H2("Modelo SIR - Epidemiologia", className="title"),
        html.Div([
            html.Label("Población Total N= "),
            dcc.Input(id="input-n-2", type = "number", value = 7138, className="input-field")
        ]),
        html.Div([
            html.Label("Tasa de transmisión (r)= "),
            dcc.Input(id="input-b-2", type = "number", value = round(1/7138,5), step=0.000001, className="input-field")
        ]),
        html.Div([
            html.Label("Tasa de recuperación (g) = "),
            dcc.Input(id="input-g-2", type = "number", value = 0.4, step=0.1, className="input-field")
        ]),
        html.Div([
            html.Label("Infectados iniciales (I)= "),
            dcc.Input(id="input-I0-2", type = "number", value = 1, className="input-field")
        ]),
        html.Div([
            html.Label("Tiempo de simulación: "),
            dcc.Input(id="input-tiempo-2", type = "number", value = 40, className="input-field")
        ]),
        
        html.Button("Generar campo", id = "btn-generar-2"),
        
        #Ejemplos
        # html.Div([
        #     html.H3("Ejemplos para probar:"),
        #     html.P("dx/dt=x, dy/dt=y"),
        #     html.P("dx/dt=-x, dy/dt=y"),
        #     html.P("dx/dt=-y, dy/dt=np.cos(x)"),
        # ])
    ], className="contain-left"),
                    dcc.Markdown(r"""
                        **Conclusión Clave:** Dado que $R_0 > 1$, la epidemia es inevitable.
                        El pico ocurre cuando los susceptibles bajan al umbral crítico $S_c = k / \beta \approx 2855$.
                    """, mathjax=True)
                ])
            ]),
            
            # --- PESTAÑA 2: RUMOR ---
            dcc.Tab(label='Caso 2: Propagación de Rumor', value='tab-2', children=[
                html.Div(className='tab-content', children=[
                    html.H3("Escenario: Rumor en la Facultad"),
                    dcc.Markdown(r"""
                        * **S (Susceptibles):** Alumnos que no han oído el rumor.
                        * **I (Infectados/Propagadores):** Alumnos que creen y difunden el rumor.
                        * **R (Racionales):** Alumnos y docentes que no creen o ya olvidaron el rumor.
                    """),

                    html.H4("Parámetros del Caso"),
                    dcc.Markdown(r"""
                        * $N = 275$
                        * $S_0 = 266$, $I_0 = 1$, $R_0 = 8$
                        * $b = 0.004$
                        * Se analizan dos tasas de "racionalidad" $k$: $0.01$ y $0.02$.
                    """, mathjax=True),

                    html.Img(src=dash.get_asset_url('grafica-rumor.png')),

                    dcc.Markdown(r"""
                        **Conclusión Clave:** El modelo muestra cómo el factor social $k$ (escepticismo,
                        olvido, intervención de autoridad) es crítico para "aplanar la curva" del rumor.
                    """, mathjax=True)
                ])
            ]),
            
            # --- PESTAÑA 3: POLÍTICA PÚBLICA ---
            dcc.Tab(label='Caso 3: Adopción de Política', value='tab-3', children=[
                html.Div(className='tab-content', children=[
                    html.H3("Escenario: Adopción de Política de Reciclaje"),
                    dcc.Markdown(r"""
                        * **S (Susceptibles):** Ciudadanos que no han adoptado la política.
                        * **I (Influyentes):** Ciudadanos que adoptaron y promueven la política.
                        * **R (Rechazadores):** Ciudadanos que deciden no adoptar la política.
                    """),

                    html.H4("Parámetros del Caso"),
                    dcc.Markdown(r"""
                        * $N = 10,050$
                        * $S_0 = 10,000$, $I_0 = 50$, $R_0 = 0$
                        * $b = 0.00005$ (Tasa de adopción)
                        * $k = 0.00002$ (Tasa de rechazo)
                    """, mathjax=True),

                    html.Img(src=dash.get_asset_url('simulacion_a3.png')),

                    dcc.Markdown(r"""
                        **Conclusión Clave:** El modelo puede simular procesos sociales lentos.
                        Permite a los planificadores estimar cómo las campañas (que afectan a $b$)
                        o las barreras (que afectan a $k$) impactan la adopción de una idea.
                    """, mathjax=True)
                ])
            ]),
            
        ]) # Fin de dcc.Tabs
        
    ]) # Fin de 'card'
]) # Fin de 'content-container'


def modelo_sir(y, t, b, g, N):
    S,I,R = y 

    dS_dt = -b*S*I
    dI_dt = b*S*I-g*I
    dR_dt = g*I

    return [dS_dt, dI_dt, dR_dt]


@callback(
    Output("grafica-sir-2", "figure")
     #Output("info-campo", "children")
     ,
     Input("btn-generar-2", "n_clicks"),
     State("input-n-2", "value"),
     State("input-b-2", "value"),
     State("input-g-2", "value"),
     State("input-I0-2", "value"),
     State("input-tiempo-2", "value"),
    prevent_initial_call=False
    )
def simular_sir(n_clicks, n, beta, gamma, I0, tiempo_max):
    S0 = n-I0 
    R0_inicial = 0
    y0 = [S0, I0, R0_inicial]
    t = np.linspace(0, tiempo_max, 500)
    try:
        solucion = odeint(modelo_sir, y0, t, args=(beta, gamma, n), full_output=False, mxstep=5000)
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