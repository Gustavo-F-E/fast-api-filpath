#from vpython import sphere, vector, rate, box
from vpython import *
from vpython.no_notebook import stop_server
# Crear objetos
box()

DELTA = 0.36959913571644626 # calculos_iniciales.py: Desfasaje angular de un ancho de paso
RADIO = 50.0
longitud_util = 150
PASO_HELICE = 84.17872144769329
ancho_eff = 19.318516525781366

# Crear los ejes cartesianos
arrow(pos=vec(0, 0, 0), axis=vec(RADIO*2, 0, 0), color=vector(1, 0, 0), shaftwidth=2)  # Eje X (rojo)
arrow(pos=vec(0, 0, 0), axis=vec(0, RADIO*2, 0), color=vector(0, 1, 0), shaftwidth=2)  # Eje Y (verde)
arrow(pos=vec(0, 0, 0), axis=vec(0, 0, RADIO*2), color=vector(0, 0, 1), shaftwidth=2)  # Eje Z (azul)

# Crear las etiquetas para los ejes
label(pos=vec(RADIO*2.2, 0, 0), text='X', color=vector(1, 0, 0), height=20, box=False, opacity=0)   # Etiqueta X (rojo)
label(pos=vec(0, RADIO*2.2, 0), text='Y', color=vector(0, 1, 0), height=20, box=False, opacity=0) # Etiqueta Y (verde)
label(pos=vec(0, 0, RADIO*2.2), text='Z', color=vector(0, 0, 1), height=20, box=False, opacity=0)  # Etiqueta Z (azul)

# Añadir otros objetos
sphere(pos=vector(0, 0, 0), radius=RADIO/10, color=vector(1, 1, 1))  # Marca el origen

cylinder(
    pos=vec(0, 0, 0),    # Posición inicial del extremo izquierdo del cilindro
    axis=vec(0, 0, longitud_util), # Dirección y longitud del cilindro
    radius=RADIO,          # Radio del cilindro
    color=vector(0.8, 0.8, 0.8),     # Color Gris claro
    opacity=0.5             # Hazlo semitransparente
)


#arco = shapes.arc(radius=RADIO, angle1=0, angle2=DELTA*10)
#arco = shapes.circle(radius=RADIO, angle1=0, angle2=DELTA, thickness=0.2, np=128)
#arco=shapes.trapezoid(pos=[0,0], width=ancho_eff, height=0.2, top=ancho_eff)
arco = shapes.circle(radius=ancho_eff, np=128)
# Crear una hélice
# Crear la trayectoria para la extrusión, usando una secuencia de puntos
helice= []

t=0 #Parametro de la curva parametrica hélice
x0 = RADIO
y0 = 0
z0 = 0
while (PASO_HELICE * t) < longitud_util:  # El número de vueltas
    x = RADIO * cos(2 * pi * t)
    y = RADIO * sin(2 * pi * t)
    z = PASO_HELICE * t
    t=t+0.1
    #helice.append(vector(x, y, z))  # Añade el punto al camino
    rate(30)
    extrusion( shape=arco, path=[vector(x0, y0, z0), vector(x, y, z)], color=vector(1, 1, 0))
    x0=x
    y0=y
    z0=z
#print(helice)
#helice=[vector(50,0,0), vector(50,0,300), vector(300,0,300)]
#extrusion( shape=arco, path=helice, color=vector(1, 1, 0))

try:
    while True: 
        rate(30)  # Controla la velocidad del bucle (30 FPS)
        # Aquí puedes agregar interactividad o condiciones de salida.
except KeyboardInterrupt:
    # Salir del bucle con Ctrl+C en la terminal
    print("Programa interrumpido por el usuario.")

# Detener el servidor de VPython
stop_server()