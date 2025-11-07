import dash 
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objects as go

dash.register_page(__name__, path="/clase5", name="Campo Vectorial")

layout = html.Div([
    html.Div([
        html.H2("Campo Vectorial", className="title"),
        html.Div([
            html.Label("Ecuación dx/dt = "),
            dcc.Input(id="input-fx", type = "text", value = "np.sin(x)", className="input-field")
        ]),
        html.Div([
            html.Label("Ecuación dy/dt = "),
            dcc.Input(id="input-fy", type = "text", value = "np.cos(x)", className="input-field")
        ]),
        html.Div([
            html.Label("Rango del Eje X = "),
            dcc.Input(id="input-xmax", type = "number", value = 5, className="input-field")
        ]),
        html.Div([
            html.Label("Rango del Eje Y = "),
            dcc.Input(id="input-ymax", type = "number", value = 5, className="input-field")
        ]),
        html.Div([
            html.Label("Mallado= "),
            dcc.Input(id="input-n", type = "number", value = 15, className="input-field")
        ]),
        
        html.Button("Generar campo", id = "btn-generar"),
        
        #Ejemplos
        html.Div([
            html.H3("Ejemplos para probar:"),
            html.P("dx/dt=x, dy/dt=y"),
            html.P("dx/dt=-x, dy/dt=y"),
            html.P("dx/dt=-y, dy/dt=np.cos(x)"),
        ])
    ], className="contain-left"),
    html.Div([
        html.H2("Visualización del Campo Vectorial", className="title"),
        dcc.Graph(id="grafica-campo", style={"height":"450","width":"100%"}),
        html.Div(id="info-campo")
    ], className="contain-right")
], className="page-container")

@callback(
    [Output("grafica-campo", "figure"),
     Output("info-campo", "children")],
     Input("btn-generar", "n_clicks"),
     State("input-fx", "value"),
     State("input-fy", "value"),
     State("input-xmax", "value"),
     State("input-ymax", "value"),
     State("input-n", "value"),
        prevent_initial_call=False
    )
def generar_campo(n_clicks, fx_str, fy_str, xmax, ymax, n):
    x=np.linspace(-xmax,xmax, n )
    y = np.linspace(-ymax,ymax,n)
    X,Y = np.meshgrid(x,y)
    info_mensaje = ""
    try:
        diccionario = {
            "x":X,
            "y":Y,
            "np":np,
            "sin":np.sin,
            "cos":np.cos,
            "tan":np.tan,
            "exp":np.exp,
            'sqrt':np.sqrt,
            'pi':np.pi,
            'e':np.e 
        }
        fx = eval(fx_str, {}, diccionario)
        fy = eval(fy_str, {}, diccionario)
        mag_max = np.max(np.sqrt(fx**2+fy**2))
        mag_min = np.min(np.sqrt(fx**2+fy**2))
        info_mensaje = f"Magnitud: min ={mag_min:.2f}, max = {mag_max:.2f}"
    except Exception as error: 
        fx = np.zeros_like(X)
        fy = np.zeros_like(Y)
        info_mensaje = f"Error en las expresiones {str(error)}"
    
    fig = go.Figure()

    for i in range(n):
        for j in range(n):
            x0,y0=X[i,j], Y[i,j]
            x1,y1 = x0+fx[i,j],y0+fy[i,j]
            fig.add_trace(go.Scatter(
                x = [x0,x1],
                y = [y0,y1],
                mode = "lines+markers",
                line = dict(color="blue", width=2),
                showlegend=False 
            ))
    fig.update_layout(
        title=dict(
            text = f"<b>Campo Vectorial:dx/dt = {fx_str}, dy/dt = {fy_str}",
            x=0.5
        ),
        xaxis_title = "x",
        yaxis_title="y",
        paper_bgcolor="lightyellow",
        plot_bgcolor="white",
        
    )
    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor = "lightpink",
        zeroline=True, zerolinewidth=2, zerolinecolor="red",
        showline=True, linecolor="black", linewidth=2, mirror=True,
        range=[-xmax*1.1,xmax*1.1]
    )
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor = "lightpink",
        zeroline=True, zerolinewidth=2, zerolinecolor="red",
        showline=True, linecolor="black", linewidth=2, mirror=True,
        range=[-ymax*1.1,ymax*1.1])
    return fig, info_mensaje