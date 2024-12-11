from shapely.geometry import Polygon, MultiPolygon
import matplotlib.pyplot as plt
import numpy as np
import math
import random
from graficar_bobinado_desplegado import graficar_bobinado_desplegado, graficar_bobinado_desplegado2, graficar_bobinado_desplegado3

def grafico_patron_elegido_2(diccionario_capa, guardar_grafico):
    
    PI = diccionario_capa["PI"]
    longitud_util = diccionario_capa["longitud_util"]
    alfa = diccionario_capa["alfa"]
    alfa_original = diccionario_capa["alfa_original"]
    radio = diccionario_capa["radio"]
    NP = diccionario_capa["NP"]
    PASO_HELICE = diccionario_capa["PASO_HELICE"]
    CANTIDAD_VUELTAS_HELICE = diccionario_capa["CANTIDAD_VUELTAS_HELICE"]
    PASO_EN_Y = diccionario_capa["PASO_EN_Y"]
    patron_elegido = diccionario_capa["patron_elegido_Nº"]
    orden_de_patrones = diccionario_capa["orden_del_patron_elegido"]
    diametro_mandril = diccionario_capa["diametro_mandril"]
    ancho = diccionario_capa["ancho"]
    uuid_6 = diccionario_capa["uuid_6"]

    puntos_ida_a0=[]
    puntos_ida_b0=[]
    puntos_ida_c0=[]
    puntos_ida_d0=[]
    areas_ida_0=[]
    puntos_vuelta_a0=[]
    puntos_vuelta_b0=[]
    puntos_vuelta_c0=[]
    puntos_vuelta_d0=[]
    areas_vuelta_0=[]
    x_min=0
    x_max=2*PI*radio
    y_incremento=x_max*math.tan(alfa)
    y_a0=0
    y_a0_vuelta=0
    for i in range(NP):
        puntos_ida_a0=(x_min, y_a0)
        puntos_ida_b0=(x_max, y_a0+y_incremento)
        puntos_ida_c0=(x_max, y_a0+y_incremento-PASO_EN_Y)
        puntos_ida_d0=(x_min, y_a0-PASO_EN_Y)
        puntos_vuelta_a0=(x_min, y_a0_vuelta)
        puntos_vuelta_b0=(x_min, y_a0_vuelta+PASO_EN_Y)
        puntos_vuelta_c0=[x_max, y_a0_vuelta+PASO_EN_Y-y_incremento]
        puntos_vuelta_d0=[x_max, y_a0_vuelta-y_incremento]
        areas_ida_0.append([puntos_ida_a0, puntos_ida_b0, puntos_ida_c0, puntos_ida_d0])
        areas_vuelta_0.append([puntos_vuelta_a0, puntos_vuelta_b0, puntos_vuelta_c0, puntos_vuelta_d0])
        y_a0=y_a0-PASO_EN_Y
        y_a0_vuelta=y_a0_vuelta+PASO_EN_Y

    bobinado_desplegado=Polygon([(0,0),(0, longitud_util),(x_max, longitud_util),(x_max, 0)])

    areas_ida = []
    areas_vuelta = []
    intersecciones_ida = []
    intersecciones_totales = []
    intersecciones_vuelta = []
    listado_total_ida=[]
    listado_total_vuelta=[]
    diccionario_areas={}
    for k in range(NP):
        y_incremento2_ida = 0
        ax_ida, ay_ida = areas_ida_0[k][0]
        bx_ida, by_ida = areas_ida_0[k][1]
        cx_ida, cy_ida = areas_ida_0[k][2]
        dx_ida, dy_ida = areas_ida_0[k][3]
        
        y_incremento2_vuelta = 0
        ax_vuelta, ay_vuelta = areas_vuelta_0[k][0]
        bx_vuelta, by_vuelta = areas_vuelta_0[k][1]
        cx_vuelta, cy_vuelta = areas_vuelta_0[k][2]
        dx_vuelta, dy_vuelta = areas_vuelta_0[k][3]

        sub_area_ida = []
        sub_area_vuelta = []
        interseccion_de_sub_area_ida = []
        interseccion_de_sub_area_vuelta = []
        
        for j in range(CANTIDAD_VUELTAS_HELICE + 2):
            puntos_ida=[(ax_ida, ay_ida + y_incremento2_ida), (bx_ida, by_ida + y_incremento2_ida), (cx_ida, cy_ida + y_incremento2_ida), (dx_ida, dy_ida + y_incremento2_ida)]
            sub_area_ida.append(puntos_ida)
            y_incremento2_ida += PASO_HELICE-PASO_EN_Y
            poligono_ida=bobinado_desplegado.intersection(Polygon(puntos_ida))
            interseccion_de_sub_area_ida.append(poligono_ida)
            intersecciones_totales.append(poligono_ida)
            listado_total_ida.append(poligono_ida)
            if not poligono_ida.is_empty:
                diccionario_areas[f"area_ida_{k+1}_{j}"]=poligono_ida
                diccionario_areas[f"area_ida_contador{k+1}"]=j

            puntos_vuelta=[(ax_vuelta, ay_vuelta + y_incremento2_vuelta), (bx_vuelta, by_vuelta + y_incremento2_vuelta), (cx_vuelta, cy_vuelta + y_incremento2_vuelta), (dx_vuelta, dy_vuelta + y_incremento2_vuelta)]
            sub_area_vuelta.append(puntos_vuelta)
            y_incremento2_vuelta += PASO_HELICE-PASO_EN_Y
            poligono_vuelta=bobinado_desplegado.intersection(Polygon(puntos_vuelta))
            interseccion_de_sub_area_vuelta.append(poligono_vuelta)
            intersecciones_totales.append(poligono_vuelta)
            listado_total_vuelta.append(poligono_vuelta)
            if not poligono_vuelta.is_empty:
                diccionario_areas[f"area_vuelta_{k+1}_{j}"]=poligono_vuelta
                diccionario_areas[f"area_vuelta_contador{k+1}"]=j

        areas_ida.append(sub_area_ida)
        areas_vuelta.append(sub_area_vuelta)
        intersecciones_ida.append(interseccion_de_sub_area_ida)
        intersecciones_vuelta.append(interseccion_de_sub_area_vuelta)
    print(diccionario_areas)
    '''
    print('areas_ida')
    print(len(areas_ida_0))
    print(areas_ida_0)
    #print(len(areas_ida))
    print(areas_ida)
    print('areas_vuelta')
    print(len(areas_vuelta_0))
    print(areas_vuelta_0)
    #print(len(areas_ida))
    print(areas_vuelta)


    intersection1 = bobinado_desplegado.intersection(Polygon(areas_ida[0][0]))  # Intersección de áreas
    intersection2 = bobinado_desplegado.intersection(Polygon(areas_ida[0][1]))  # Intersección de áreas
    intersection3 = bobinado_desplegado.intersection(Polygon(areas_ida[0][2]))  # Intersección de áreas
    intersections=[intersection1,intersection2,intersection3]

    graficar_bobinado_desplegado(intersection1, x_max, longitud_util, 'intersection', colors='blue')
    graficar_bobinado_desplegado(intersection2, x_max, longitud_util, 'intersection', colors='red')
    graficar_bobinado_desplegado(intersection3, x_max, longitud_util, 'intersection', colors='green')
    graficar_bobinado_desplegado(intersections, x_max, longitud_util, 'intersection')

    graficar_bobinado_desplegado(intersecciones_ida[0], x_max, longitud_util, 'intersecciones ida 1')
    graficar_bobinado_desplegado(intersecciones_ida[22], x_max, longitud_util, 'intersecciones ida 23')
    graficar_bobinado_desplegado(intersecciones_ida[44], x_max, longitud_util, 'intersecciones ida 45')
    print('intersecciones_ida[44]')
    print(intersecciones_ida[44])

    graficar_bobinado_desplegado(listado_total_ida, x_max, longitud_util, 'intersecciones ida', colors='green')
    graficar_bobinado_desplegado(listado_total_vuelta, x_max, longitud_util, 'intersecciones vuelta', colors='blue')
    '''
    listado_total_ida2 = listado_total_ida[:-2] # Elimina los dos últimos elementos
    listado_total_vuelta2 = listado_total_vuelta[:-2]  # Elimina los dos últimos elementos
    '''
    graficar_bobinado_desplegado(listado_total_ida2, x_max, longitud_util, 'intersecciones totales ida', colors='green')
    graficar_bobinado_desplegado(listado_total_vuelta2, x_max, longitud_util, 'intersecciones totales vuelta', colors='blue')

    print('listado_total_vuelta2')
    print(listado_total_vuelta2)
    print('listado_total_vuelta2')
    print(len(listado_total_vuelta2))

    lista_del_patron=[]
    for i in range(NP):
        index=orden_de_patrones[i]
        lista_del_patron.append(intersecciones_ida[index-1])
        lista_del_patron.append(intersecciones_vuelta[index-1])

    print('lista_del_patron')
    print(lista_del_patron)

    # Aplanar la lista usando una comprensión de listas
    lista_del_patron = [polygon for sublist in lista_del_patron for polygon in sublist]

    print('lista_del_patron')
    print(lista_del_patron)
    print('len(lista_del_patron)')
    print(len(lista_del_patron))



    # Limpia la lista eliminando los polígonos vacíos
    lista_limpia = [
        [poligono for poligono in sublista if not poligono.is_empty]
        for sublista in lista_del_patron
    ]

    print(lista_limpia)

    graficar_bobinado_desplegado(lista_del_patron[0], x_max, longitud_util, 'intersecciones totales', alternate=True)
    graficar_bobinado_desplegado(lista_del_patron[1], x_max, longitud_util, 'intersecciones totales', alternate=True)
    graficar_bobinado_desplegado(lista_del_patron[2], x_max, longitud_util, 'intersecciones totales', alternate=True)
    graficar_bobinado_desplegado(lista_del_patron[3], x_max, longitud_util, 'intersecciones totales', alternate=True)
    graficar_bobinado_desplegado(lista_del_patron[4], x_max, longitud_util, 'intersecciones totales', alternate=True)
    graficar_bobinado_desplegado(lista_del_patron[5], x_max, longitud_util, 'intersecciones totales', alternate=True)
    '''


    graficar_bobinado_desplegado2(listado_total_ida2, listado_total_vuelta2, x_max, longitud_util, NP, CANTIDAD_VUELTAS_HELICE, orden_de_patrones, alfa, alfa_original, radio, PI, PASO_HELICE, patron_elegido, diametro_mandril, ancho, uuid_6, guardar_grafico)
    
    graficar_bobinado_desplegado3(diccionario_capa, guardar_grafico, diccionario_areas)