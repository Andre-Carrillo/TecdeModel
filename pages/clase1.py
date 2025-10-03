import dash
from dash import html, dcc

dash.register_page(__name__, path="/clase1", name="clase1")

layout = html.Div([
    html.H1("Bienvenido a la clase1"),
])