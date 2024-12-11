import matplotlib.pyplot as plt
import math

def dibujar_area(puntos, ax, color, N):
    # Separar las coordenadas X e Y de los puntos
    x, y = zip(*puntos)
    
    # Dibujar el polígono cerrando la figura al unir el primer y último punto
    ax.fill(x, y, color, edgecolor='black')  # Relleno con el color especificado y bordes negros

    # Configurar límites del gráfico si es necesario (opcional)
    ax.set_xlim(0, N)
    ax.set_ylim(0, N)

# Llamar a la función para generar las áreas
def areas_patron(N):
    x0 = []
    xN = []
    y0 = []
    yN = []
    for i in range(0, N + 1):
        x0.append((0, i))
        xN.append((N, i))
        y0.append((i, 0))
        yN.append((i, N))
    
    areas_x = []
    areas_y = []
    for k in range(0, N):
        kx=k
        ky=N-1-k
        areas_x.append([y0[kx], yN[kx], yN[kx + 1], y0[kx + 1]])  # Llenamos áreas x
        areas_y.append([x0[ky], x0[ky + 1], xN[ky + 1], xN[ky]])  # Llenamos áreas y
    
    return areas_x, areas_y

def graficar_multiples_areas(lista_de_areas, N, paso, index2, orden, ptr, Dcco, diccionario_capa, guardar_grafico, graficar_solo_esquemas):
    diametro_mandril = diccionario_capa["diametro_mandril"]
    ancho = diccionario_capa["ancho"]
    uuid_6 = diccionario_capa["uuid_6"]
    longitud_util = diccionario_capa["longitud_util"]
    alfa = diccionario_capa["alfa"]
    alfa_original = diccionario_capa["alfa_original"]
    NP = diccionario_capa["NP"]
    # Crear la figura y el eje una sola vez
    fig, ax = plt.subplots()
    # Iterar sobre la lista de áreas con el índice
    for index, puntos in enumerate(lista_de_areas):
        # Verificar si el índice es par o impar
        if index % 2 == 0:
            dibujar_area(puntos, ax, 'blue', N)
            # Código para manejar el caso par
        else:
            dibujar_area(puntos, ax, 'red', N)
            # Código para manejar el caso impar

    # Etiquetar los ejes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    
    # Dividir el vector "orden" en tramos de 20
    lineas_orden = [orden[i:i + 20] for i in range(0, len(orden), 20)]

    # Convertir cada tramo en una cadena y unirlas con saltos de línea
    texto_orden = "\n".join([", ".join(map(str, linea)) for linea in lineas_orden])
    
    # Añadir el título
    ax.set_title(f"Patrón Nº {index2+1}; NP = {N}; paso = {paso}; Ptr = {ptr}; Dcco = {Dcco}")
    # Subtítulo en múltiples líneas usando variables
    ax.text(
    0.5, -0.2,  # Ajusta la posición del subtítulo en Y para que quede justo debajo del título
    f"Orden de los patrones:\n[{texto_orden}]",
    ha='center', va='top', transform=ax.transAxes,
    fontsize=10  # Tamaño de fuente opcional
    )
    # Ajustar el espacio inferior para asegurar que el subtítulo se muestre
    plt.subplots_adjust(bottom=0.2)
    
    # Mostrar y/o guardar el gráfico
    if graficar_solo_esquemas==True:
        nombre_archivo=f"imagenes/patrones/NP={NP}_esquema_patron_Nº_{index2}_.png"
    else: 
        nombre_archivo=f"imagenes/diam_{diametro_mandril}_long={longitud_util}_ancho={ancho}_alfa={alfa_original}_{uuid_6}_NP={NP}_esquema_patron_Nº_{index2+1}_.png"
    
    if guardar_grafico:
        plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')  # Guarda el gráfico como PNG
        #print(f"Gráfico guardado como: {nombre_archivo}")
    
    # Mostrar el gráfico con todas las áreas
    plt.show()
    #Quitar el grafico

def orden_de_listas_areas(N, ORDEN):
    areas_x, areas_y = areas_patron(N)
    lista_areas = []
    
    for i in range(len(ORDEN)):  # Ajustar índice
        lista_areas.append(areas_y[ORDEN[i] - 1])
        lista_areas.append(areas_x[ORDEN[i] - 1])
    #print(lista_areas)
    return lista_areas