import math
import numpy as np

def trayectoria_1(alfa, ds, longitud_util, radio):
    dz = ds * math.cos(alfa)
    
    # Inicializa 'z' como una lista vacía y genera los valores
    z_trayectoria_1 = np.arange(0, longitud_util, dz)

    # Verifica si el último valor es igual a 'zfg'
    if z_trayectoria_1[-1] != longitud_util:
        z_trayectoria_1 = np.append(z_trayectoria_1, longitud_util)

    # Cálculos
    c = radio / np.tan(alfa)
    phi_trayectoria_1 = z_trayectoria_1 / c  # Se define la variable 'phi'
    x_trayectoria_1 = radio * np.cos(phi_trayectoria_1)  # Se define la variable 'x'
    y_trayectoria_1 = radio * np.sin(phi_trayectoria_1)  # Se define la variable 'y'
    
    #longitud_trayectoria_1 = np.sqrt((phi * radio) ** 2 + (z) ** 2)
    #print(f"x={x}\n y={y}\n z={z}\n longitud_trayectoria_1={longitud_trayectoria_1}\n")
    
    return x_trayectoria_1, y_trayectoria_1, z_trayectoria_1, phi_trayectoria_1, c
