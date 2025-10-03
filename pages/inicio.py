import dash
from dash import html, dcc
import numpy as np
import plotly.graph_objects as go

dash.register_page(__name__, path="/", name="Inicio")

layout = html.Div([
    html.H1("Bienvenidos :D", style={"text-align":"center"}),
    html.Div(children=[
        html.Img(
            src="https://i.redd.it/lnzptjk79zj81.jpg",
            style={"flex":1, "width":"500px", "border-radius":"5px"}
        ),
        dcc.Markdown(
            """
                # 👋 Sobre mí  

                Hola, soy **André**, apasionado por la ciencia de datos, la inteligencia artificial y el desarrollo de software. 🚀  

                Me interesan especialmente los temas de:  
                - 📊 **Simulación y modelos matemáticos**  
                - 🤖 **Machine Learning & AI** 
                - 🔬 **Investigación y experimentación**  

                Actualmente estoy:  
                - Construyendo un portafolio de proyectos en **Python y SQL**  
                - Explorando técnicas de **visualización de datos**  
                - Aprendiendo más sobre **optimización y modelos lineales**  

                Fuera del mundo tech disfruto de:  
                - 📚 Leer y aprender constantemente  
                - 🎻 Escuchar y tocar música 
                - 🏕️ Campamentos y Trekking  
  

            """,
            style={"flex":1}, className="card"
        )
    ], style={"display":"flex"}),
    html.Div(children=[
        dcc.Markdown("""
                    # Particles Life

                    **Particles Life** es un proyecto interactivo desarrollado en **p5.js** que simula el comportamiento dinámico de partículas en un espacio bidimensional. Cada partícula sigue reglas físicas sencillas como **atracción, repulsión, velocidad y fricción**, creando patrones visuales complejos que evolucionan con el tiempo.

                    ## Características principales

                    - **Movimiento dinámico:** Las partículas se desplazan de manera fluida, respondiendo a fuerzas aplicadas.
                    - **Interacción visual:** La trayectoria y posición de cada partícula generan efectos estéticos atractivos.
                    - **Control de parámetros:** Puedes modificar variables como:
                    - Velocidad de las partículas
                    - Radio de influencia
                    - Factores de atracción o repulsión
                    - **Simulación en tiempo real:** El sistema se actualiza constantemente, mostrando un flujo continuo de partículas.


                    **Particles Life** combina la **simulación física** y el **arte generativo**, ofreciendo un entorno visualmente atractivo que permite explorar cómo reglas simples pueden generar comportamientos complejos.
 
                    """, style={"flex":1}, className="card"),
        html.Iframe(src="https://editor.p5js.org/andrecarrillomontero/full/wclvB0wkw", style={"flex":1, "height":"600px"})
    ], style={"display":"flex"})
])