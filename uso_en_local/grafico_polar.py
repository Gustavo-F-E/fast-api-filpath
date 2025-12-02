import os
import numpy as np
import matplotlib.pyplot as plt
import math

def grafico_polar(txt):
    """
    Lee un archivo .txt y extrae los valores numéricos entre 'X ' y ' Y'.
    
    Args:
        txt (str): Ruta al archivo .txt.
    
    Returns:
        np.array: Vector numérico con los valores extraídos.
    """
    # Verificar si el archivo existe
    if not os.path.exists(txt):
        raise FileNotFoundError(f"El archivo '{txt}' no existe.")
    
    valores = []  # Lista para almacenar los valores extraídos en radianes

    # Leer el archivo línea por línea
    with open(txt, 'r') as file:
        for linea in file:
            # Buscar el valor entre 'X ' y ' Y'
            if 'X ' in linea and ' Y' in linea:
                try:
                    # Extraer el valor numérico
                    inicio = linea.index('X ') + 2  # Posición después de 'X '
                    fin = linea.index(' Y')         # Posición antes de ' Y'
                    valor = float(linea[inicio:fin].strip())  # Convertir a float
                    # Convertir a grados
                    valores.append(valor)  # Agregar el valor en radianes a la lista
                except ValueError:
                    print(f"Advertencia: No se pudo convertir a número en la línea: {linea.strip()}")
    
    # Convertir la lista a un array de NumPy y retornarlo
    print(f"Valores extraídos en radianes: \n {valores}")

    # Filtrar los valores: i=1 y luego i=i+8
    valores_filtrados = valores[1::8]

    for i in range(len(valores_filtrados)):
        if valores_filtrados[i] > 2*math.pi:
            valores_filtrados[i] = valores_filtrados[i] - (int(valores_filtrados[i] / (2 * math.pi))) * (2 * math.pi)

    valores_deg_filtrados = []  # Lista para almacenar los valores extraídos en grados
    for i in range(len(valores_filtrados)):
        valores_deg_filtrados.append(math.degrees(valores_filtrados[i]))

    print(f"Valores filtrados en radianes: \n {valores_filtrados}")
    print(f"Valores filtrados en grados: \n {valores_deg_filtrados}")
    print(f"{len(valores_filtrados)}")

        # Crear el gráfico polar
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

    # Crear un array de radios con la misma longitud que valores_filtrados
    radios = np.ones(len(valores_filtrados))  # Radio constante para todos los puntos

    ax.plot(valores_filtrados, radios, 'bo-', linewidth=2)  # 'bo-' es línea azul con puntos
    
    ax.set_yticks([])  # Ocultar los números en el eje radial
    ax.grid(False)     # Desactivar la grilla interna
    
    # Ajustar el título con margen inferior
    ax.set_title('Gráfico Polar', va='bottom', fontsize=14, pad=40, fontweight='bold')  # `pad` ajusta el margen inferior

    # Agregar texto al lado de cada punto
    for idx, (angulo, radio) in enumerate(zip(valores_filtrados, radios)):
        # Convertir el ángulo de radianes a grados para la rotación
        angulo_grados = math.degrees(angulo)
        
        # Ajustar la alineación del texto según el ángulo
        if 90 < angulo_grados < 270:  # Si el ángulo está en la mitad inferior
            ha = 'right'
            rotation = angulo_grados + 180  # Invertir el texto
        else:  # Si el ángulo está en la mitad superior
            ha = 'left'
            rotation = angulo_grados
        if idx == len(valores_filtrados) - 1:
            ax.text(
                angulo, 
                radio + 0.02, 
                f'[{idx+1}º - {valores_deg_filtrados[idx]:.2f}º]', 
                fontsize=8, 
                color='red', 
                ha=ha,  # Alineación horizontal
                va='center',  # Alineación vertical
                rotation=rotation,  # Rotar el texto según el ángulo
                rotation_mode='anchor'  # Rotar alrededor del punto de anclaje
            )
        else:
            ax.text(
                angulo, 
                radio + 0.02, 
                f'\n \n [{idx+1}º - {valores_deg_filtrados[idx]:.2f}º]', 
                fontsize=8, 
                color='red', 
                ha=ha,  # Alineación horizontal
                va='center',  # Alineación vertical
                rotation=rotation,  # Rotar el texto según el ángulo
                rotation_mode='anchor'  # Rotar alrededor del punto de anclaje
            )

    # Mostrar el gráfico
    plt.show()

grafico_polar('corridas/diam=154_long=740_ancho=17.5_Capa_Unica_capa_3_55_4ae527.txt')