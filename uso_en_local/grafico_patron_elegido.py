import matplotlib.pyplot as plt
import math
import numpy as np

def grafico_patron_elegido(diccionario_capa, guardar_grafico):

    PI = diccionario_capa["PI"]
    longitud_util = diccionario_capa["longitud_util"]
    alfa = diccionario_capa["alfa"]
    alfa_original = diccionario_capa["alfa_original"]
    radio = diccionario_capa["radio"]
    NP = diccionario_capa["NP"]
    PASO_HELICE = diccionario_capa["PASO_HELICE"]
    CANTIDAD_VUELTAS_HELICE = diccionario_capa["CANTIDAD_VUELTAS_HELICE"]
    PASO_EN_Y = diccionario_capa["PASO_EN_Y"]
    vector_X_cara_a = diccionario_capa["vector_X_cara_a"]
    patron_elegido = diccionario_capa["patron_elegido_Nº"]
    orden_de_patrones = diccionario_capa["orden_del_patron_elegido"]
    diametro_mandril = diccionario_capa["diametro_mandril"]
    ancho = diccionario_capa["ancho"]
    uuid_6 = diccionario_capa["uuid_6"]
    
    # Calcular puntos en X para las caras A y B
    XA = vector_X_cara_a
    XA.append(2*PI*radio)  # Agregar el último punto en XA

    YA = [i * PASO_EN_Y for i in range(NP + 1)]  # Generar valores YA
    YA.append(PASO_HELICE)  # Agregar el último punto en XA
    
    # Generar áreas para graficar
    AREAS_IDA = []
    AREAS_VUELTA = []
    # Graficar áreas
    fig, ax = plt.subplots()
    # Etiquetas de los ejes
    ax.set_xlabel("Eje X (Rad * Radio) [mm]")
    ax.set_ylabel("Eje Y (Long. Mandril) [mm]")
    for secuencia in orden_de_patrones:
        NP=len(orden_de_patrones)
        #print(secuencia)
        #print(NP)
        secuencia=secuencia-1
        #print(secuencia)
        # Área entre XA e YB
        if CANTIDAD_VUELTAS_HELICE>0:

            LONGITUD_IRREGULAR=longitud_util-CANTIDAD_VUELTAS_HELICE*PASO_HELICE

            for i in range(CANTIDAD_VUELTAS_HELICE):
                area_regular_ida(secuencia, NP, XA, YA, i, PASO_HELICE, AREAS_IDA, ax)

            for j in range(CANTIDAD_VUELTAS_HELICE):
                area_regular_vuelta(secuencia, NP, XA, YA, j, PASO_HELICE, AREAS_VUELTA, ax)
            
            area_irregular_ida(secuencia, XA, PASO_HELICE, AREAS_IDA, ax, CANTIDAD_VUELTAS_HELICE, LONGITUD_IRREGULAR, alfa, PI, radio)
            
            maxX, maxY = area_irregular_vuelta(secuencia, XA, PASO_HELICE, AREAS_VUELTA, ax, CANTIDAD_VUELTAS_HELICE, LONGITUD_IRREGULAR, alfa, PI, radio)
        else:
            LONGITUD_IRREGULAR=longitud_util
            
            area_irregular_ida(secuencia, XA, PASO_HELICE, AREAS_IDA, ax, CANTIDAD_VUELTAS_HELICE, LONGITUD_IRREGULAR, alfa, PI, radio)
            
            maxX, maxY = area_irregular_vuelta(secuencia, XA, PASO_HELICE, AREAS_VUELTA, ax, CANTIDAD_VUELTAS_HELICE, LONGITUD_IRREGULAR, alfa, PI, radio)

    #print(AREAS_IDA)
    #print(AREAS_VUELTA)
    
    #limX=100*math.ceil(maxX/100)
    #limY=100*math.ceil(maxY/100)
    limX=maxX
    limY=maxY
    # Supón que tienes datos que se extienden hasta estos límites
    ax.set_xlim(0, limX)
    ax.set_ylim(0, limY)

    # Ajusta la relación de aspecto para que el gráfico respete la escala entre X e Y
    ax.set_aspect(limY/limX)  # Usa la relación Y/X
    # Título principal del gráfico
    ax.set_title(f'Gráfico de secuencia de Áreas. Patrón elegido: Nº {patron_elegido}', pad=30)

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
    
    # Crear el eje X secundario usando secondary_xaxis
    def primary_to_secondary(x):
        return (x / limX) * 360  # Transformación a 0-360 grados
    
    def secondary_to_primary(x):
        return (x / 360) * limX  # Transformación inversa
    
    ax2 = ax.secondary_xaxis('top', functions=(primary_to_secondary, secondary_to_primary))
    ax2.set_xlabel("Eje X [Grados]")
    
    # Invertir ambos ejes x
    ax.invert_xaxis()
    ax2.invert_xaxis()
    
    # Mostrar y/o guardar el gráfico
    nombre_archivo=f"imagenes/diam_{diametro_mandril}_long={longitud_util}_ancho={ancho}_alfa={alfa_original}_{uuid_6}_grafico_patron_Nº_{patron_elegido}_.png"
    
    if guardar_grafico:
        plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')  # Guarda el gráfico como PNG
        #print(f"Gráfico guardado como: {nombre_archivo}")
    
    plt.show()

def area_regular_ida(secuencia, NP, XA, YA, i, PASO_HELICE, AREAS_IDA, ax):
    if secuencia!=NP:
        area_ida_1 = [
            (XA[secuencia], YA[0]+PASO_HELICE*i),
            (XA[secuencia + 1], YA[0]+PASO_HELICE*i),
            (XA[NP], YA[NP-secuencia-1]+PASO_HELICE*i),
            (XA[NP], YA[NP-secuencia]+PASO_HELICE*i)
        ]
    else:
        area_ida_1 = [
            (XA[secuencia-1], YA[0]+PASO_HELICE*i),
            (XA[secuencia], YA[0])+PASO_HELICE*i,
            (XA[NP],YA[NP-secuencia-1]+PASO_HELICE*i)
        ]
    AREAS_IDA.append(area_ida_1)
    xs, ys = zip(*area_ida_1)  # Separar coordenadas X e Y
    ax.fill(xs, ys, 'b', edgecolor='black', linewidth=0.5)  # Rellenar área ida con azul

    # Área entre XA e YB
    if secuencia==0:
        area_ida_2 = [
            (XA[0], YA[NP]+PASO_HELICE*i),
            (XA[secuencia+1], YA[NP]+PASO_HELICE*i),
            (XA[0], YA[NP-secuencia-1]+PASO_HELICE*i)
        ]
    else:
        area_ida_2 = [
            (XA[0], YA[NP-secuencia]+PASO_HELICE*i),
            (XA[secuencia], YA[NP]+PASO_HELICE*i),
            (XA[secuencia+1], YA[NP]+PASO_HELICE*i),
            (XA[0], YA[NP-secuencia-1]+PASO_HELICE*i)
        ]
    AREAS_IDA.append(area_ida_2)
    xs, ys = zip(*area_ida_2)  # Separar coordenadas X e Y
    ax.fill(xs, ys, 'b', edgecolor='black', linewidth=0.5)  # Rellenar área ida con azul

def area_regular_vuelta(secuencia, NP, XA, YA, j, PASO_HELICE, AREAS_VUELTA, ax):
    if secuencia==NP:
        area_vuelta_1 = [
            (XA[NP], YA[NP]+PASO_HELICE*j),
            (XA[NP], YA[NP-1]+PASO_HELICE*j),
            (XA[NP-1], YA[NP]+PASO_HELICE*j),
        ]
    else:
        area_vuelta_1 = [
            (XA[secuencia], YA[NP]+PASO_HELICE*j),
            (XA[secuencia + 1], YA[NP]+PASO_HELICE*j),
            (XA[NP], YA[secuencia+1]+PASO_HELICE*j),
            (XA[NP], YA[secuencia]+PASO_HELICE*j)
        ]
    AREAS_VUELTA.append(area_vuelta_1)
    xs, ys = zip(*area_vuelta_1)  # Separar coordenadas X e Y
    ax.fill(xs, ys, 'r', edgecolor='black', linewidth=0.5)  # Rellenar área vuelta con rojo

    if secuencia==0:
        area_vuelta_2 = [
            (XA[0], YA[0]+PASO_HELICE*j),
            (XA[0], YA[1]+PASO_HELICE*j),
            (XA[1], YA[0]),
        ]
    else:
        area_vuelta_2 = [
            (XA[secuencia], YA[0]+PASO_HELICE*j),
            (XA[0], YA[secuencia]+PASO_HELICE*j),
            (XA[0], YA[secuencia+1]+PASO_HELICE*j),
            (XA[secuencia+1], YA[0]+PASO_HELICE*j)
        ]
    AREAS_VUELTA.append(area_vuelta_2)
    xs, ys = zip(*area_vuelta_2)  # Separar coordenadas X e Y
    ax.fill(xs, ys, 'r', edgecolor='black', linewidth=0.5)  # Rellenar área vuelta con rojo

def area_irregular_ida(secuencia, XA, PASO_HELICE, AREAS_IDA, ax, CANTIDAD_VUELTAS_HELICE, LONGITUD_IRREGULAR, alfa, PI, radio):

    a=XA[secuencia]
    b=XA[secuencia+1]
    a1=a+math.tan(alfa)*LONGITUD_IRREGULAR
    b1=b+math.tan(alfa)*LONGITUD_IRREGULAR
    
    maxX=2*PI*radio #Máximo Limite en el eje X
    minY=CANTIDAD_VUELTAS_HELICE*PASO_HELICE
    maxY=minY+LONGITUD_IRREGULAR #Máximo Limite en el eje Y
    
    delta_X1=b1-maxX
    delta_Y1=delta_X1/math.tan(alfa)
    
    if b<maxX and a1<maxX and b1<=maxX:
        area_ida_1 = [
            (a, minY),
            (b, minY),
            (b1, maxY),
            (a1, maxY)
        ]
        AREAS_IDA.append(area_ida_1)
        xs, ys = zip(*area_ida_1)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'b', edgecolor='black', linewidth=0.5)  # Rellenar área ida con azul
    
    if b==maxX and a1==maxX and delta_Y1==LONGITUD_IRREGULAR:
        area_ida_1 = [
            (a, minY),
            (b, minY),
            (maxX, maxY)
        ]
        AREAS_IDA.append(area_ida_1)
        xs, ys = zip(*area_ida_1)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'b', edgecolor='black', linewidth=0.5)  # Rellenar área ida con azul
        
        area_ida_2 = [
            (0, minY),
            (b1-b, maxY),
            (0, maxY),
        ]
        AREAS_IDA.append(area_ida_2)
        xs, ys = zip(*area_ida_2)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'b', edgecolor='black', linewidth=0.5)  # Rellenar área ida con azul
    
    if b<=maxX and a1<maxX and b1>maxX:
        
        area_ida_1 = [
            (a, minY),
            (b, minY),
            (maxX, maxY-delta_Y1),
            (maxX, maxY),
            (a1, maxY)
        ]
        AREAS_IDA.append(area_ida_1)
        xs, ys = zip(*area_ida_1)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'b', edgecolor='black', linewidth=0.5)  # Rellenar área ida con azul
        
        area_ida_2 = [
            (0, maxY-delta_Y1),
            (delta_X1, maxY),
            (0, maxY),
        ]
        AREAS_IDA.append(area_ida_2)
        xs, ys = zip(*area_ida_2)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'b', edgecolor='black', linewidth=0.5)  # Rellenar área ida con azul
    
    if b<=maxX and a1>maxX and b1>maxX:
        c=(maxX-b)/math.tan(alfa)
        d=(maxX-a)/math.tan(alfa)
        extremo=(b-a)/math.tan(alfa)
        if d>extremo:
            area_ida_1 = [
                (a, minY),
                (b, minY),
                (maxX, minY+c),
                (maxX, minY+d)
            ]
            AREAS_IDA.append(area_ida_1)
            xs, ys = zip(*area_ida_1)  # Separar coordenadas X e Y
            ax.fill(xs, ys, 'b', edgecolor='black', linewidth=0.5)  # Rellenar área ida con azul
            area_ida_2 = [
                (0, minY+c),
                (0, minY+d),
                (a1-maxX, maxY),
                (b1-maxX, maxY)
            ]
            AREAS_IDA.append(area_ida_2)
            xs, ys = zip(*area_ida_2)  # Separar coordenadas X e Y
            ax.fill(xs, ys, 'b', edgecolor='black', linewidth=0.5)  # Rellenar área ida con azul
        
        if d<=extremo:
            area_ida_1 = [
                (a, minY),
                (maxX, minY),
                (maxX, d)
            ]
            AREAS_IDA.append(area_ida_1)
            xs, ys = zip(*area_ida_1)  # Separar coordenadas X e Y
            ax.fill(xs, ys, 'b', edgecolor='black', linewidth=0.5)  # Rellenar área ida con azul
            area_ida_2 = [
                (0, minY+0),
                (0, minY+d),
                (a1-maxX, maxY),
                (b1-maxX, maxY)
            ]
            AREAS_IDA.append(area_ida_2)
            xs, ys = zip(*area_ida_2)  # Separar coordenadas X e Y
            ax.fill(xs, ys, 'b', edgecolor='black', linewidth=0.5)  # Rellenar área ida con azul

def area_irregular_vuelta(secuencia, XA, PASO_HELICE, AREAS_VUELTA, ax, CANTIDAD_VUELTAS_HELICE, LONGITUD_IRREGULAR, alfa, PI, radio):
    maxX=2*PI*radio #Máximo Limite en el eje X
    minY=CANTIDAD_VUELTAS_HELICE*PASO_HELICE
    maxY=minY+LONGITUD_IRREGULAR #Máximo Limite en el eje Y
    
    a=XA[secuencia]
    b=XA[secuencia+1]
    a1=a-math.tan(alfa)*LONGITUD_IRREGULAR
    b1=b-math.tan(alfa)*LONGITUD_IRREGULAR
    a2=a-math.tan(alfa)*LONGITUD_IRREGULAR+maxX
    b2=b-math.tan(alfa)*LONGITUD_IRREGULAR+maxX
    adyacente1=a/math.tan(alfa)
    adyacente2=b/math.tan(alfa)

    
    if secuencia==0 and (minY+adyacente2)>maxY:
        xi=(adyacente2-LONGITUD_IRREGULAR)*math.tan(alfa)
        xii=LONGITUD_IRREGULAR*math.tan(alfa)
        area_vuelta_1 = [
            (0, minY),
            (b, minY),
            (xi, maxY),
            (0, maxY),
        ]
        AREAS_VUELTA.append(area_vuelta_1)
        xs, ys = zip(*area_vuelta_1)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'r', edgecolor='black', linewidth=0.5)  # Rellenar área ida con azul
        
        area_vuelta_2 = [
            (maxX, minY),
            (maxX, maxY),
            (maxX-xii, maxY),
        ]
        AREAS_VUELTA.append(area_vuelta_2)
        xs, ys = zip(*area_vuelta_2)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'r', edgecolor='black', linewidth=0.5)  # Rellenar área ida con azul
    
    if secuencia==0 and (minY+adyacente2)==maxY:
        xi=LONGITUD_IRREGULAR*math.tan(alfa)
        area_vuelta_1 = [
            (0, minY),
            (b, minY),
            (0, maxY),
        ]
        AREAS_VUELTA.append(area_vuelta_1)
        xs, ys = zip(*area_vuelta_1)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'r', edgecolor='black', linewidth=0.5)  # Rellenar área ida con azul
        
        area_vuelta_2 = [
            (maxX, minY),
            (maxX, maxY),
            (maxX-xi, maxY),
        ]
        AREAS_VUELTA.append(area_vuelta_2)
        xs, ys = zip(*area_vuelta_2)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'r', edgecolor='black', linewidth=0.5)  # Rellenar área ida con azul
    
    if secuencia==0 and (minY+adyacente2)<maxY:
        xi=maxX-math.tan(alfa)*(LONGITUD_IRREGULAR-adyacente2)
        xii=maxX-math.tan(alfa)*(LONGITUD_IRREGULAR)
        area_vuelta_1 = [
            (0, minY),
            (b, minY),
            (0, minY+adyacente2)
        ]
        AREAS_VUELTA.append(area_vuelta_1)
        xs, ys = zip(*area_vuelta_1)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'r', edgecolor='black', linewidth=0.5)  # Rellenar área ida con azul
        
        area_vuelta_2 = [
            (maxX, minY),
            (maxX, minY+adyacente2),
            (xi, maxY),
            (xii, maxY),
        ]
        AREAS_VUELTA.append(area_vuelta_2)
        xs, ys = zip(*area_vuelta_2)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'r', edgecolor='black', linewidth=0.5)  # Rellenar área ida con azul

    if secuencia!=0 and (minY+adyacente2)>maxY and (minY+adyacente1)<maxY:
        yi=a/math.tan(alfa)
        yii=maxY-yi
        xi=maxX-yii*math.tan(alfa)
        area_vuelta_1 = [
            (a, minY),
            (b, minY),
            (b1, maxY),
            (0, maxY),
            (0, minY+yi)
        ]
        AREAS_VUELTA.append(area_vuelta_1)
        xs, ys = zip(*area_vuelta_1)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'r', edgecolor='black', linewidth=0.5)  # Rellenar área ida con azul
        
        area_vuelta_2 = [
            (maxX, minY+yi),
            (maxX, maxY),
            (a2, maxY)
        ]
        AREAS_VUELTA.append(area_vuelta_2)
        xs, ys = zip(*area_vuelta_2)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'r', edgecolor='black', linewidth=0.5)  # Rellenar área ida con azul

    if secuencia!=0 and (minY+adyacente2)>maxY and (minY+adyacente1)>maxY:
        area_vuelta_1 = [
            (a, minY),
            (b, minY),
            (b1, maxY),
            (a1, maxY),
        ]
        AREAS_VUELTA.append(area_vuelta_1)
        xs, ys = zip(*area_vuelta_1)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'r', edgecolor='black', linewidth=0.5)  # Rellenar área ida con azul
    
    if secuencia!=0 and (minY+adyacente2)<maxY and (minY+adyacente1)<maxY:
        area_vuelta_1 = [
            (a, minY),
            (b, minY),
            (0, minY+adyacente2),
            (0, minY+adyacente1),
        ]
        AREAS_VUELTA.append(area_vuelta_1)
        xs, ys = zip(*area_vuelta_1)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'r', edgecolor='black', linewidth=0.5)  # Rellenar área ida con azul
        
        area_vuelta_2 = [
            (maxX, minY+adyacente1),
            (maxX, minY+adyacente2),
            (b2, maxY),
            (a2, maxY)
        ]
        AREAS_VUELTA.append(area_vuelta_2)
        xs, ys = zip(*area_vuelta_2)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'r', edgecolor='black', linewidth=0.5)  # Rellenar área ida con azul
    return(maxX, maxY)

