import numpy as np
import math
import os
import matplotlib.pyplot as plt
import re

def generar_serie(primer_valor, valor_maximo):
    # Inicializar la serie
    serie = []
    serie.append(primer_valor)  # Comenzar con el primer valor
    contador = 1
    
    while True:
        # Calcular el siguiente incremento basado en la posición
        if contador % 4 == 0:
            incremento = 3  # Aumento de 3 cada 4 términos
        else:
            incremento = 2  # Aumento de 2 en los demás casos
        
        # Calcular el siguiente valor
        siguiente_valor = serie[contador - 1] + incremento
        
        # Salir del bucle si el siguiente valor excede el valor máximo
        if siguiente_valor > valor_maximo:
            break
        
        # Agregar el siguiente valor a la serie
        serie.append(siguiente_valor)
        contador += 1
    
    return serie

def lector_txt(txt, radio, pi):
    cadena_concatenada = f"{txt}.txt"
    
    # Abre el archivo de texto para lectura
    with open(cadena_concatenada, 'r') as file:
        lineas_txt = file.readlines()
    
    # Inicializa la estructura para almacenar valores
    valores = {
        'txt': lineas_txt,
        'XX': [],
        'YY': [],
        'AA': [],
        'FF': []
    }

    valores['XX'].append(0)
    valores['YY'].append(0)
    valores['AA'].append(0)
    valores['FF'].append(0)
    
    # Expresión regular para extraer los valores
    regex = re.compile(r'X\s*([-+]?\d*\.\d+|\d+)\s*Y\s*([-+]?\d*\.\d+|\d+)\s*A\s*([-+]?\d*\.\d+|\d+)\s*F\s*([-+]?\d*\.\d+|\d+)')
    
    # Itera a través de las líneas
    for linea in lineas_txt:
        match = regex.search(linea)
        
        if match:
            xx = float(match.group(1))
            yy = float(match.group(2))
            aa = float(match.group(3))
            ff = float(match.group(4))
            valores['XX'].append(xx)
            valores['YY'].append(yy)
            valores['AA'].append(aa)
            valores['FF'].append(ff)
    
    #valores['X'], valores['Y'], valores['A'], valores['F'] = redimensionar_vector(valores['XX'], valores['YY'], valores['AA'], valores['FF'])
    valores['X'], valores['Y'], valores['A'], valores['F'] = valores['XX'], valores['YY'], valores['AA'], valores['FF']

    valores['X_radianes_1'] = np.array(valores['X'])
    valores['X_grados_1'] = valores['X_radianes_1'] * (180 / pi)
    
    valores['X_grados_2'] = np.array(valores['XX']) * (180 / pi)
    
    valores['X_giros'] = valores['X_radianes_1'] / (2 * pi)
    valores['X_giros_int'] = np.floor(valores['X_giros']).astype(int)
    valores['X_rad_absolutos'] = valores['X_radianes_1'] - (valores['X_giros_int'] * (2 * pi))
    valores['X_gr_vueltas'] = np.floor(valores['X_grados_1'] / 360)
    
    return valores

# Asegúrate de definir las funciones 'generar_serie' y 'redimensionar_vector' en tu código

def graficar_dos_vectores(x, y, txt):
    # Graficar
    plt.figure()  # Crea una nueva figura

    # Grafica con línea continua, marcador de círculo lleno y línea más gruesa
    plt.plot(x, y, '-+', linewidth=2, markersize=5, markerfacecolor='b')
    
    # Título del gráfico con texto más grande
    plt.title('Gráfico del Eje X vs. Eje Y', fontsize=16)

    # Añadir un subtítulo
    plt.suptitle(f'Archivo: "{txt}.txt" \n ', fontsize=12)
    
    # Ajustar el límite del eje Y para que el subtítulo sea visible
    plt.ylim([-1, 11])
    
    # Etiqueta para el eje X con texto más grande
    plt.xlabel('Eje X [rad]', fontsize=12)
    
    # Etiqueta para el eje Y con texto más grande
    plt.ylabel('Eje Y [mm]', fontsize=12)
    
    # Activa la cuadrícula
    plt.grid(True)

    XMIN = min(x) - 10
    XMAX = max(x) + 10

    YMIN = min(y) - 20
    YMAX = max(y) + 20

    plt.xlim([XMIN, XMAX])  # Limites del eje X entre XMIN y XMAX
    plt.ylim([YMIN, YMAX])  # Limites del eje Y entre YMIN e YMAX

    # Añadir texto en las posiciones especificadas si existen suficientes elementos
    if len(x) > 1 and len(y) > 1:
        plt.text(x[1], y[1], f'X: {x[1]:.2f} \n Y: {y[1]:.2f}', verticalalignment='bottom', horizontalalignment='left', fontsize=10, fontweight='bold', color='r')
    if len(x) > 2 and len(y) > 2:
        plt.text(x[2], y[2], f'X: {x[2]:.2f} \n Y: {y[2]:.2f}', verticalalignment='bottom', horizontalalignment='right', fontsize=10, fontweight='bold', color='r')
    if len(x) > 4 and len(y) > 4:
        plt.text(x[4], y[4], f'X: {x[4]:.2f} \n Y: {y[4]:.2f}', verticalalignment='top', horizontalalignment='left', fontsize=10, fontweight='bold', color='r')
    if len(x) > 5 and len(y) > 5:
        plt.text(x[5], y[5], f'X: {x[5]:.2f} \n Y: {y[5]:.2f}', verticalalignment='top', horizontalalignment='right', fontsize=10, fontweight='bold', color='r')
    
    # Ajusta el tamaño de los ejes
    plt.gca().tick_params(axis='both', which='major', labelsize=12)  # Aumenta el tamaño de los números de los ejes

    # Establecer el tamaño de la figura (opcional)
    plt.gcf().set_size_inches(12, 6)  # Anchura y altura de la figura en pulgadas

    # Exportar la figura a un archivo PNG con alta resolución
    plt.savefig(f"{txt}.png", dpi=600)  # 'dpi=600' es la resolución (600 DPI)
    #plt.close()

uuid_6 = "a4b739"

# Define el nombre del archivo sin la extensión
#txt1 = f"diam=100_long=550_ancho=5.5_Capa_1_corrida_prueba_mandril_pines_alambre_{uuid_6}"
#txt2= f"diam=100_long=550_ancho=5.5_Capa_2_corrida_prueba_mandril_pines_alambre_{uuid_6}"
#txt3 = f"diam=100_long=550_ancho=5.5_Total_corrida_prueba_mandril_pines_alambre_{uuid_6}"

#txt = "diam=100_long=550_ancho=5.5_Total_corrida_prueba_mandril_pines_alambre_853bb8"
txt1 = f"diam=100_long=550_ancho=5.5_Capa_Unica_corrida_prueba_mandril_pines_alambre_{uuid_6}"

radio = 100 / 2

pi = math.pi

# Llama a la función lector_txt con el nombre del archivo y guarda el resultado en una variable
#valores = lector_txt(txt, radio, pi)
valores1 = lector_txt(txt1, radio, pi)
#valores2 = lector_txt(txt2, radio, pi)
#valores3 = lector_txt(txt3, radio, pi)

# Llama a la función graficar_dos_vectores con los valores y el nombre del archivo
#graficar_dos_vectores(valores['X'], valores['Y'], txt)

graficar_dos_vectores(valores1['X'], valores1['Y'], txt1)
#graficar_dos_vectores(valores2['X'], valores2['Y'], txt2)
#graficar_dos_vectores(valores3['X'], valores3['Y'], txt3)
