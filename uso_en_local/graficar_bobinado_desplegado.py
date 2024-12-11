import matplotlib.pyplot as plt
from shapely.geometry import Polygon, MultiPolygon


def graficar_bobinado_desplegado(polygons, x_max, longitud_util, labels=None, colors=None, alternate=False):
    """
    Graficar una lista de polígonos y/o multipolígonos.
    """
    #print("Contenido de polygons:", polygons)
    #print("Tipo de cada elemento:", [type(p) for p in polygons])
    
    # Asegurarnos de trabajar solo con polígonos válidos
    if isinstance(polygons, Polygon):  # Si es un solo polígono, lo convertimos a una lista
        polygons = [polygons]
    
    # Filtramos los polígonos válidos
    #valid_polygons = [polygon for polygon in polygons if polygon.is_valid and not polygon.is_empty]
    
    valid_polygons = [polygon for polygon in polygons if isinstance(polygon, Polygon) and polygon.is_valid and not polygon.is_empty]

    fig, ax = plt.subplots()
    '''
    # Dibujar cada polígono
    for polygon in valid_polygons:
        x, y = polygon.exterior.xy
        ax.fill(x, y, alpha=0.5, fc=colors if colors else 'r', edgecolor='black')  # Puedes personalizar 'fc' con los colores si se pasa como parámetro
    '''
    # Dibujar cada polígono
    for i, polygon in enumerate(valid_polygons):
        x, y = polygon.exterior.xy
        
        # Si alternate es True, alternar entre rojo y azul
        if alternate:
            color = 'red' if i % 2 == 0 else 'blue'  # Alterna entre rojo y azul
        else:
            # Usar el color pasado como argumento, si existe
            color = colors if colors else 'r'  # Si no se pasa un color, usar 'r' como predeterminado
        
        # Pinta las áreas con el color seleccionado
        ax.fill(x, y, fc=color, edgecolor='black')

    # Agregar etiquetas si se proporcionan
    '''
    if labels:
        for i, polygon in enumerate(valid_polygons):
            # Obtener el centroide del polígono
            if polygon.centroid.is_valid:
                x, y = polygon.centroid.x, polygon.centroid.y
                ax.text(x, y, str(labels[i]), color='black', fontsize=8)
    '''
    
    # Establecer los límites de los ejes si se especifican
    ax.set_xlim([0, x_max])
    ax.set_ylim([0, longitud_util])
    
    # Invertir el eje X
    ax.set_xlim(ax.get_xlim()[::-1])  # Esto invierte el rango del eje X

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(labels)
    plt.grid(True)
    plt.show()

def graficar_bobinado_desplegado2(listado_total_ida2, listado_total_vuelta2, x_max, longitud_util, NP, CANTIDAD_VUELTAS_HELICE, orden_de_patrones, alfa, alfa_original, radio, PI, PASO_HELICE, patron_elegido, diametro_mandril, ancho, uuid_6, guardar_grafico):
    """
    Graficar una lista de polígonos y/o multipolígonos.
    """
    
    # Asegurarnos de trabajar solo con polígonos válidos
    if isinstance(listado_total_ida2, Polygon):  # Si es un solo polígono, lo convertimos a una lista
        listado_total_ida2 = [listado_total_ida2]
    if isinstance(listado_total_vuelta2, Polygon):  # Si es un solo polígono, lo convertimos a una lista
        listado_total_vuelta2 = [listado_total_vuelta2]
    fig, ax = plt.subplots()
    for i in range(NP):
        index = orden_de_patrones[i] - 1  # Ajuste del índice a base 0
        for k in range(2):
            if k == 0:
                for j in range(CANTIDAD_VUELTAS_HELICE + 2):
                    try:
                        polygon1 = listado_total_ida2[index * (CANTIDAD_VUELTAS_HELICE + 2) + j]
                        if not polygon1.is_empty:
                            x, y = polygon1.exterior.xy
                            ax.fill(x, y, fc='blue', edgecolor='black', linewidth=0.5)
                    except IndexError:
                        pass  # Si el índice está fuera de rango, ignorar
            if k == 1:
                for j in range(CANTIDAD_VUELTAS_HELICE + 2):
                    try:
                        polygon2 = listado_total_vuelta2[index * (CANTIDAD_VUELTAS_HELICE + 2) + j]
                        if not polygon2.is_empty:
                            x, y = polygon2.exterior.xy
                            ax.fill(x, y, fc='red', edgecolor='black', linewidth=0.5)
                    except IndexError:
                        pass  # Si el índice está fuera de rango, ignorar

    # Establecer los límites de los ejes si se especifican
    ax.set_xlim([0, x_max])
    ax.set_ylim([0, longitud_util])
    
    # Ajusta la relación de aspecto para que el gráfico respete la escala entre X e Y
    ax.set_aspect(longitud_util/x_max)  # Usa la relación Y/X
    
    # Subtítulo en múltiples líneas usando variables
    ax.text(
    0.5, -0.2,  # Ajusta la posición del subtítulo en Y para que quede justo debajo del título
    f"Longitud útil = {longitud_util} mm; Ángulo = {round(alfa*180/PI)}; Radio = {radio} mm; Cantidad de ciclos = {NP};\n"
    f"Cantidad de vueltas de la hélice = {CANTIDAD_VUELTAS_HELICE}; Paso de la hélice = {PASO_HELICE} mm",
    ha='center', va='top', transform=ax.transAxes,
    fontsize=10  # Tamaño de fuente opcional
    )
    
    # Ajustar el espacio del gráfico para que el subtítulo no se superponga
    plt.subplots_adjust(bottom=0.2)  # Aumenta el valor según sea necesario

    # Añadir asíntotas amarillas
    for i in range(1, CANTIDAD_VUELTAS_HELICE + 1):
        y = i * PASO_HELICE
        ax.axhline(y=y, color=(0.56, 0.93, 0.56), linestyle='--', linewidth=3)
    
    # Crear el eje X secundario usando secondary_xaxis
    def primary_to_secondary(x):
        return (x / x_max) * 360  # Transformación a 0-360 grados
    
    def secondary_to_primary(x):
        return (x / 360) * x_max  # Transformación inversa
    
    ax2 = ax.secondary_xaxis('top', functions=(primary_to_secondary, secondary_to_primary))
    ax2.set_xlabel("Eje X [Grados]")
    
    # Invertir ambos ejes x
    ax.invert_xaxis()
    ax2.invert_xaxis()
    
    # Crear el segundo eje Y
    def primary_to_secondary_y(y):
        return y / PASO_HELICE

    def secondary_to_primary_y(y):
        return y * PASO_HELICE

    ax2 = ax.secondary_yaxis('right', functions=(primary_to_secondary_y, secondary_to_primary_y))
    ax2.set_ylabel("Eje Y (Número de Vueltas)")
    
    # Etiquetas de los ejes
    ax.set_xlabel("Eje X (Rad * Radio) [mm]")
    ax.set_ylabel("Eje Y (Long. Mandril) [mm]")
    plt.title(f"Gráfico del Patrón elegido (Nº {patron_elegido})")
    plt.grid(False)
    # Mostrar y/o guardar el gráfico
    nombre_archivo=f"imagenes/diam_{diametro_mandril}_long={longitud_util}_ancho={ancho}_alfa={alfa_original}_{uuid_6}_grafico2_patron_Nº_{patron_elegido}_.png"
    
    if guardar_grafico:
        plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')  # Guarda el gráfico como PNG
        #print(f"Gráfico guardado como: {nombre_archivo}")
    plt.show()


def graficar_bobinado_desplegado3(diccionario_capa, guardar_grafico, diccionario_areas):
    
    PI = diccionario_capa["PI"]
    longitud_util = diccionario_capa["longitud_util"]
    alfa = diccionario_capa["alfa"]
    alfa_original = diccionario_capa["alfa_original"]
    radio = diccionario_capa["radio"]
    NP = diccionario_capa["NP"]
    PASO_HELICE = diccionario_capa["PASO_HELICE"]
    CANTIDAD_VUELTAS_HELICE = diccionario_capa["CANTIDAD_VUELTAS_HELICE"]
    patron_elegido = diccionario_capa["patron_elegido_Nº"]
    orden_de_patrones = diccionario_capa["orden_del_patron_elegido"]
    diametro_mandril = diccionario_capa["diametro_mandril"]
    ancho = diccionario_capa["ancho"]
    uuid_6 = diccionario_capa["uuid_6"]
    x_max=2*PI*radio
    
    fig, ax = plt.subplots()
    for k in range(NP):
        orden=orden_de_patrones[k]
        imax=diccionario_areas[f"area_ida_contador{orden}"]
        jmax=diccionario_areas[f"area_vuelta_contador{orden}"]
        for i in range(imax+1):
            poligono_ida=diccionario_areas[f"area_ida_{orden}_{i}"]
            x, y = poligono_ida.exterior.xy
            ax.fill(x, y, fc='blue', edgecolor='black', linewidth=0.5)
        for j in range(jmax+1):
            poligono_vuelta=diccionario_areas[f"area_vuelta_{orden}_{j}"]
            x, y = poligono_vuelta.exterior.xy
            ax.fill(x, y, fc='red', edgecolor='black', linewidth=0.5)
    
    # Establecer los límites de los ejes si se especifican
    ax.set_xlim([0, x_max])
    ax.set_ylim([0, longitud_util])
    
    # Ajusta la relación de aspecto para que el gráfico respete la escala entre X e Y
    ax.set_aspect(longitud_util/x_max)  # Usa la relación Y/X
    
    # Subtítulo en múltiples líneas usando variables
    ax.text(
    0.5, -0.2,  # Ajusta la posición del subtítulo en Y para que quede justo debajo del título
    f"Longitud útil = {longitud_util} mm; Ángulo = {round(alfa*180/PI)}; Radio = {radio} mm; Cantidad de ciclos = {NP};\n"
    f"Cantidad de vueltas de la hélice = {CANTIDAD_VUELTAS_HELICE}; Paso de la hélice = {PASO_HELICE} mm",
    ha='center', va='top', transform=ax.transAxes,
    fontsize=10  # Tamaño de fuente opcional
    )
    
    # Ajustar el espacio del gráfico para que el subtítulo no se superponga
    plt.subplots_adjust(bottom=0.2)  # Aumenta el valor según sea necesario

    # Añadir asíntotas verdes
    for i in range(1, CANTIDAD_VUELTAS_HELICE + 1):
        y = i * PASO_HELICE
        ax.axhline(y=y, color=(0.56, 0.93, 0.56), linestyle='--', linewidth=3)
    
    # Crear el eje X secundario usando secondary_xaxis
    def primary_to_secondary(x):
        return (x / x_max) * 360  # Transformación a 0-360 grados
    
    def secondary_to_primary(x):
        return (x / 360) * x_max  # Transformación inversa
    
    ax2 = ax.secondary_xaxis('top', functions=(primary_to_secondary, secondary_to_primary))
    ax2.set_xlabel("Eje X [Grados]")
    
    # Invertir ambos ejes x
    ax.invert_xaxis()
    ax2.invert_xaxis()
    
    # Crear el segundo eje Y
    def primary_to_secondary_y(y):
        return y / PASO_HELICE

    def secondary_to_primary_y(y):
        return y * PASO_HELICE

    ax2 = ax.secondary_yaxis('right', functions=(primary_to_secondary_y, secondary_to_primary_y))
    ax2.set_ylabel("Eje Y (Número de Vueltas)")
    
    # Etiquetas de los ejes
    ax.set_xlabel("Eje X (Rad * Radio) [mm]")
    ax.set_ylabel("Eje Y (Long. Mandril) [mm]")
    plt.title(f"Gráfico del Patrón elegido (Nº {patron_elegido})")
    plt.grid(False)
    # Mostrar y/o guardar el gráfico
    nombre_archivo=f"imagenes/diam_{diametro_mandril}_long={longitud_util}_ancho={ancho}_alfa={alfa_original}_{uuid_6}_grafico2_patron_Nº_{patron_elegido}_.png"
    
    if guardar_grafico:
        plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')  # Guarda el gráfico como PNG
        #print(f"Gráfico guardado como: {nombre_archivo}")
    plt.show()