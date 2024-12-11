import matplotlib.pyplot as plt
import math

PI = math.pi
radio=50.0
NP=35
PASO_HELICE=314.1592653589794
orden_de_patrones=[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34]
vector_X_cara_a=[0.0, 8.975979010256552, 17.951958020513104, 26.927937030769655, 35.90391604102621, 44.87989505128276, 53.85587406153931, 62.83185307179586, 71.80783208205241, 80.78381109230897, 89.75979010256552, 98.73576911282207, 107.71174812307862, 116.68772713333517, 125.66370614359172, 134.6396851538483, 143.61566416410483, 152.59164317436137, 161.56762218461793, 170.5436011948745, 179.51958020513104, 188.49555921538757, 197.47153822564414, 206.4475172359007, 215.42349624615724, 224.39947525641378, 233.37545426667035, 242.3514332769269, 251.32741228718345, 260.30339129744, 269.2793703076966, 278.2553493179531, 287.23132832820966, 296.2073073384662, 305.18328634872273]
PASO_EN_Y=8.975979010256554
CANTIDAD_VUELTAS_HELICE=2
alfa=0.7853981633974483
#longitud_util = 300 #Longitud útil del patrón
longitud_util = 5 #Longitud útil del patrón

PASO_HELICE=314.1592653589794


def grafico_patron_elegido(PI, radio, NP, PASO_HELICE, orden_de_patrones, vector_X_cara_a, PASO_EN_Y, CANTIDAD_VUELTAS_HELICE, alfa, longitud_util):
    
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
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Gráfico de secuencia de  Áreas')
    for secuencia in orden_de_patrones:
        NP=len(orden_de_patrones)
        print(secuencia)
        print(NP)
        secuencia=secuencia-1
        print(secuencia)
        # Área entre XA e YB
        if CANTIDAD_VUELTAS_HELICE>0:

            LONGITUD_IRREGULAR=longitud_util-CANTIDAD_VUELTAS_HELICE*PASO_HELICE

            for i in range(CANTIDAD_VUELTAS_HELICE):
                area_regular_ida(secuencia, NP, XA, YA, i, PASO_HELICE, AREAS_IDA, ax)

            for j in range(CANTIDAD_VUELTAS_HELICE):
                area_regular_vuelta(secuencia, NP, XA, YA, j, PASO_HELICE, AREAS_VUELTA, ax)
            
            area_irregular_ida(secuencia, XA, PASO_HELICE, AREAS_IDA, ax, CANTIDAD_VUELTAS_HELICE, LONGITUD_IRREGULAR, alfa, PI, radio)
            
            area_irregular_vuelta(secuencia, XA, PASO_HELICE, AREAS_VUELTA, ax, CANTIDAD_VUELTAS_HELICE, LONGITUD_IRREGULAR, alfa, PI, radio)
        else:
            LONGITUD_IRREGULAR=longitud_util
            
            area_irregular_ida(secuencia, XA, PASO_HELICE, AREAS_IDA, ax, CANTIDAD_VUELTAS_HELICE, LONGITUD_IRREGULAR, alfa, PI, radio)
            
            area_irregular_vuelta(secuencia, XA, PASO_HELICE, AREAS_VUELTA, ax, CANTIDAD_VUELTAS_HELICE, LONGITUD_IRREGULAR, alfa, PI, radio)

    print(AREAS_IDA)
    print(AREAS_VUELTA)

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
    ax.fill(xs, ys, 'b', edgecolor='black')  # Rellenar área ida con azul

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
    ax.fill(xs, ys, 'b', edgecolor='black')  # Rellenar área ida con azul

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
    ax.fill(xs, ys, 'r', edgecolor='black')  # Rellenar área vuelta con rojo

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
    ax.fill(xs, ys, 'r', edgecolor='black')  # Rellenar área vuelta con rojo


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
        ax.fill(xs, ys, 'b', edgecolor='black')  # Rellenar área ida con azul
    
    if b==maxX and a1==maxX and delta_Y1==LONGITUD_IRREGULAR:
        area_ida_1 = [
            (a, minY),
            (b, minY),
            (maxX, maxY)
        ]
        AREAS_IDA.append(area_ida_1)
        xs, ys = zip(*area_ida_1)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'b', edgecolor='black')  # Rellenar área ida con azul
        
        area_ida_2 = [
            (0, minY),
            (b1-b, maxY),
            (0, maxY),
        ]
        AREAS_IDA.append(area_ida_2)
        xs, ys = zip(*area_ida_2)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'b', edgecolor='black')  # Rellenar área ida con azul
    
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
        ax.fill(xs, ys, 'b', edgecolor='black')  # Rellenar área ida con azul
        
        area_ida_2 = [
            (0, maxY-delta_Y1),
            (delta_X1, maxY),
            (0, maxY),
        ]
        AREAS_IDA.append(area_ida_2)
        xs, ys = zip(*area_ida_2)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'b', edgecolor='black')  # Rellenar área ida con azul
    
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
            ax.fill(xs, ys, 'b', edgecolor='black')  # Rellenar área ida con azul
            area_ida_2 = [
                (0, minY+c),
                (0, minY+d),
                (a1-maxX, maxY),
                (b1-maxX, maxY)
            ]
            AREAS_IDA.append(area_ida_2)
            xs, ys = zip(*area_ida_2)  # Separar coordenadas X e Y
            ax.fill(xs, ys, 'b', edgecolor='black')  # Rellenar área ida con azul
        
        if d<=extremo:
            area_ida_1 = [
                (a, minY),
                (maxX, minY),
                (maxX, minY+d)
            ]
            AREAS_IDA.append(area_ida_1)
            xs, ys = zip(*area_ida_1)  # Separar coordenadas X e Y
            ax.fill(xs, ys, 'b', edgecolor='black')  # Rellenar área ida con azul
            area_ida_2 = [
                (0, minY+0),
                (0, minY+d),
                (a1-maxX, maxY),
                (b1-maxX, maxY)
            ]
            AREAS_IDA.append(area_ida_2)
            xs, ys = zip(*area_ida_2)  # Separar coordenadas X e Y
            ax.fill(xs, ys, 'b', edgecolor='black')  # Rellenar área ida con azul


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
        ax.fill(xs, ys, 'r', edgecolor='black')  # Rellenar área ida con azul
        
        area_vuelta_2 = [
            (maxX, minY),
            (maxX, maxY),
            (maxX-xii, maxY),
        ]
        AREAS_VUELTA.append(area_vuelta_2)
        xs, ys = zip(*area_vuelta_2)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'r', edgecolor='black')  # Rellenar área ida con azul
    
    if secuencia==0 and (minY+adyacente2)==maxY:
        xi=LONGITUD_IRREGULAR*math.tan(alfa)
        area_vuelta_1 = [
            (0, minY),
            (b, minY),
            (0, maxY),
        ]
        AREAS_VUELTA.append(area_vuelta_1)
        xs, ys = zip(*area_vuelta_1)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'r', edgecolor='black')  # Rellenar área ida con azul
        
        area_vuelta_2 = [
            (maxX, minY),
            (maxX, maxY),
            (maxX-xi, maxY),
        ]
        AREAS_VUELTA.append(area_vuelta_2)
        xs, ys = zip(*area_vuelta_2)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'r', edgecolor='black')  # Rellenar área ida con azul
    
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
        ax.fill(xs, ys, 'r', edgecolor='black')  # Rellenar área ida con azul
        
        area_vuelta_2 = [
            (maxX, minY),
            (maxX, minY+adyacente2),
            (xi, maxY),
            (xii, maxY),
        ]
        AREAS_VUELTA.append(area_vuelta_2)
        xs, ys = zip(*area_vuelta_2)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'r', edgecolor='black')  # Rellenar área ida con azul

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
        ax.fill(xs, ys, 'r', edgecolor='black')  # Rellenar área ida con azul
        
        area_vuelta_2 = [
            (maxX, minY+yi),
            (maxX, maxY),
            (a2, maxY)
        ]
        AREAS_VUELTA.append(area_vuelta_2)
        xs, ys = zip(*area_vuelta_2)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'r', edgecolor='black')  # Rellenar área ida con azul

    if secuencia!=0 and (minY+adyacente2)>maxY and (minY+adyacente1)>maxY:
        area_vuelta_1 = [
            (a, minY),
            (b, minY),
            (b1, maxY),
            (a1, maxY),
        ]
        AREAS_VUELTA.append(area_vuelta_1)
        xs, ys = zip(*area_vuelta_1)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'r', edgecolor='black')  # Rellenar área ida con azul
    
    if secuencia!=0 and (minY+adyacente2)<maxY and (minY+adyacente1)<maxY:
        area_vuelta_1 = [
            (a, minY),
            (b, minY),
            (0, minY+adyacente2),
            (0, minY+adyacente1),
        ]
        AREAS_VUELTA.append(area_vuelta_1)
        xs, ys = zip(*area_vuelta_1)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'r', edgecolor='black')  # Rellenar área ida con azul
        
        area_vuelta_2 = [
            (maxX, minY+adyacente1),
            (maxX, minY+adyacente2),
            (b2, maxY),
            (a2, maxY)
        ]
        AREAS_VUELTA.append(area_vuelta_2)
        xs, ys = zip(*area_vuelta_2)  # Separar coordenadas X e Y
        ax.fill(xs, ys, 'r', edgecolor='black')  # Rellenar área ida con azul

while longitud_util<PASO_HELICE:
    grafico_patron_elegido(PI, radio, NP, PASO_HELICE, orden_de_patrones, vector_X_cara_a, PASO_EN_Y, CANTIDAD_VUELTAS_HELICE, alfa, longitud_util)
    longitud_util=longitud_util+10