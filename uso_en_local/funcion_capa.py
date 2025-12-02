import math
import json
import uuid
import os
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, MultiPolygon

# Constantes por defecto
DIAMETRO_MANDRIL_DEFAULT = 100
LONGITUD_UTIL_DEFAULT = 360
ALFA_DEFAULT = 45
ANCHO_DEFAULT = 6.5
EXCESO_DE_RESINA_DEFAULT = False
CORREGIR_ANGULO_DEFAULT = False
PINES_DEFAULT = False
COEFICIENTE_ROZAMIENTO_DEFAULT = 0.2
ESPESOR_DEFAULT = 0.2
VELOCIDAD_DE_ALIMENTACION_DEFAULT = 9000


def crear_diccionario_capa(
    diametro_mandril=DIAMETRO_MANDRIL_DEFAULT,
    longitud_util=LONGITUD_UTIL_DEFAULT,
    alfa=ALFA_DEFAULT,
    ancho=ANCHO_DEFAULT,
    exceso_de_resina=EXCESO_DE_RESINA_DEFAULT,
    corregir_angulo=CORREGIR_ANGULO_DEFAULT,
    pines=PINES_DEFAULT,
    coeficiente_rozamiento=COEFICIENTE_ROZAMIENTO_DEFAULT,
    espesor=ESPESOR_DEFAULT,
    velocidad_de_alimentacion=VELOCIDAD_DE_ALIMENTACION_DEFAULT
):
    """
    Crea un diccionario con los parámetros de la capa.
    
    Args:
        diametro_mandril: Diámetro del mandril
        longitud_util: Longitud útil
        alfa: Ángulo alfa
        ancho: Ancho
        exceso_de_resina: Si hay exceso de resina
        corregir_angulo: Si se debe corregir el ángulo
        pines: Si hay pines
        coeficiente_rozamiento: Coeficiente de rozamiento
        espesor: Espesor
        velocidad_de_alimentacion: Velocidad de alimentación
    
    Returns:
        dict: Diccionario con los parámetros de la capa
    """
    uuid_aleatorio = str(uuid.uuid4())
    uuid_6 = uuid_aleatorio[:6]
    filename = f"diam_{diametro_mandril}_long={longitud_util}_ancho={ancho}_alfa={alfa}_{uuid_6}.json"
    filename2 = f"diam_{diametro_mandril}_long={longitud_util}_ancho={ancho}_alfa={alfa}_{uuid_6}"
    
    diccionario_capa = {
        "filename": filename,
        "filename2": filename2,
        "uuid_6": uuid_6,
        "PI": math.pi,
        "diametro_mandril": diametro_mandril,
        "longitud_util": longitud_util,
        "alfa": alfa,
        "alfa_original": alfa,
        "ancho": ancho,
        "exceso_de_resina": exceso_de_resina,
        "corregir_angulo": corregir_angulo,
        "pines": pines,
        "coeficiente_rozamiento": coeficiente_rozamiento,
        "espesor": espesor,
        "velocidad_de_alimentacion": velocidad_de_alimentacion
    }
    
    return diccionario_capa


def guardar_json(diccionario_capa):
    """
    Guarda el diccionario de la capa en un archivo JSON.
    
    Args:
        diccionario_capa: Diccionario con los parámetros de la capa
    
    Returns:
        str: Nombre del archivo creado o None si hubo error
    """
    filename = diccionario_capa["filename"]
    try:
        with open(filename, 'w') as json_file:
            json.dump(diccionario_capa, json_file, indent=4)
        print(f"Archivo JSON '{filename}' creado exitosamente.")
        return filename
    except Exception as e:
        print(f"Error al crear el archivo JSON: {e}")
        return None


def calculos_iniciales(diccionario_capa):
    
    PI = diccionario_capa["PI"]
    diametro_mandril = diccionario_capa["diametro_mandril"]
    alfa = diccionario_capa["alfa"]
    ancho = diccionario_capa["ancho"]
    exceso_de_resina = diccionario_capa["exceso_de_resina"]
    corregir_angulo = diccionario_capa["corregir_angulo"]
    pines = diccionario_capa["pines"]
    
    if pines==True:
        longitud_util = diccionario_capa["longitud_util"]+20
        coeficiente_rozamiento = 5
    else:
        longitud_util = diccionario_capa["longitud_util"]
        coeficiente_rozamiento = diccionario_capa["coeficiente_rozamiento"]
    
    alfa=math.radians(alfa)
    ancho_eff = ancho / math.cos(alfa) #Ancho efectivo de las fibras
    radio = diametro_mandril/2
    #Correción del ángulo
    if corregir_angulo==False and exceso_de_resina==False:
        NP = math.ceil(2 * PI * radio / ancho_eff) #Número de pasadas sin corregir (tiene superposicion)
    if corregir_angulo==False and exceso_de_resina==True:
        NP = math.floor(2 * PI * radio / ancho_eff) #Número de pasadas corregidas (sin superposicion y con exceso de resina)
    if corregir_angulo==True and exceso_de_resina==False:
        #Lógica para saber si el ángulo corregido lo debo aumentar o disminuir
        NP = 2 * PI * radio / ancho_eff
        NP_floor = math.floor(2 * PI * radio / ancho_eff)
        NP_ceil = math.ceil(2 * PI * radio / ancho_eff)
        if (NP_ceil-NP) < (NP-NP_floor):
            ancho_eff=(2 * PI * radio)/NP_ceil
            NP = NP_ceil
        else:
            ancho_eff=(2 * PI * radio)/NP_floor
            NP = NP_floor
        alfa=math.acos(ancho/ancho_eff) #Cálculo del ángulo corregido
    if corregir_angulo==True and exceso_de_resina==True:
        NP=1/0
    DELTA=2*PI/NP #Desfasaje angular de un ancho de paso
    PASO_HELICE=2*PI*radio/math.tan(alfa)
    # Calcular paso en Y
    PASO_EN_Y = PASO_HELICE / NP
    #print(f"longitud_util/PASO_HELICE={longitud_util/PASO_HELICE}")
    CANTIDAD_VUELTAS_HELICE=math.floor(longitud_util/PASO_HELICE) #Cantidad de vueltas completas de la helice
    if CANTIDAD_VUELTAS_HELICE>0:
        DIFERENCIA=longitud_util-PASO_HELICE*CANTIDAD_VUELTAS_HELICE #Longitud de la Fraccion de vueltas que no son completas
    else:
        DIFERENCIA=longitud_util-PASO_HELICE
    DESFASAJE=DIFERENCIA*math.tan(alfa)/radio #Cuanto se desfasa angularmente en la fraccion no completa
    
    vector_X_cara_a=[]
    angulos_cara_a=[]
    contador_a=0
    for i in range(0,NP):
        angulos_cara_a.append(contador_a)
        vector_X_cara_a.append(contador_a*radio)
        contador_a=contador_a+DELTA
    
    vector_X_cara_b_arriba=[]
    angulos_cara_b_arriba=[]
    contador_b_arriba=DESFASAJE
    for j in range(0,NP):
        angulos_cara_b_arriba.append(contador_b_arriba)
        vector_X_cara_b_arriba.append(contador_b_arriba*radio)
        contador_b_arriba=contador_b_arriba+DELTA
        if contador_b_arriba>2*PI:
            contador_b_arriba=contador_b_arriba-2*PI
    
    vector_X_cara_b_abajo=[]
    angulos_cara_b_abajo=[]
    contador_b_abajo=2*PI-DESFASAJE
    for j in range(0,NP):
        angulos_cara_b_abajo.append(contador_b_abajo)
        vector_X_cara_b_abajo.append(contador_b_abajo*radio)
        contador_b_abajo=contador_b_abajo+DELTA
        if contador_b_abajo>2*PI:
            contador_b_abajo=contador_b_abajo-2*PI

    L_retorno=(radio/coeficiente_rozamiento)*(1-(math.sin(alfa))**2)/((math.sin(alfa))*((1-(math.sin(alfa))**2)**0.5))
    TITA_retorno=(1/coeficiente_rozamiento)*(math.log(math.sin(alfa)/(1-((1-(math.sin(alfa))**2)**0.5))))
    
    if CANTIDAD_VUELTAS_HELICE>0:
        DIFERENCIA2=longitud_util-PASO_HELICE*CANTIDAD_VUELTAS_HELICE #Longitud de la Fraccion de vueltas que no son completas
    else:
        DIFERENCIA2=longitud_util
    k0=DIFERENCIA2*math.tan(alfa)
    k1=k0+TITA_retorno
    k2=-k0-TITA_retorno
    while k2<k1:
        k2=k2+2*PI
    DWELL_3=k2-k1
    k3=TITA_retorno
    k4=-TITA_retorno
    while k4<k3:
        k4=k4+2*PI
    DWELL_8=k4-k3
    

    diccionario_capa["alfa"] = alfa
    diccionario_capa["alfa_corregido"] = alfa*180/PI
    diccionario_capa["ancho_eff"] = ancho_eff
    diccionario_capa["radio"] = radio
    diccionario_capa["NP"] = NP
    diccionario_capa["DELTA"] = DELTA
    diccionario_capa["PASO_HELICE"] = PASO_HELICE
    diccionario_capa["CANTIDAD_VUELTAS_HELICE"] = CANTIDAD_VUELTAS_HELICE
    diccionario_capa["PASO_EN_Y"] = PASO_EN_Y
    diccionario_capa["DIFERENCIA"] = DIFERENCIA
    diccionario_capa["DESFASAJE"] = DESFASAJE
    diccionario_capa["angulos_cara_a"] = angulos_cara_a
    diccionario_capa["angulos_cara_b_arriba"] = angulos_cara_b_arriba
    diccionario_capa["angulos_cara_b_abajo"] = angulos_cara_b_abajo
    diccionario_capa["vector_X_cara_a"] = vector_X_cara_a
    diccionario_capa["vector_X_cara_b_arriba"] = vector_X_cara_b_arriba
    diccionario_capa["vector_X_cara_b_abajo"] = vector_X_cara_b_abajo
    diccionario_capa["L_retorno"] = L_retorno
    diccionario_capa["TITA_retorno"] = TITA_retorno
    diccionario_capa["DWELL_3"] = DWELL_3
    diccionario_capa["DWELL_8"] = DWELL_8
    
    # Obtener el nombre del archivo
    filename = diccionario_capa["filename"]
    
    # Crear la lista de cálculos iniciales
    calculos_iniciales = [
        {"alfa": alfa},
        {"alfa_corregido": alfa * 180 / PI},
        {"ancho_eff": ancho_eff},
        {"radio": radio},
        {"NP": NP},
        {"DELTA": DELTA},
        {"PASO_HELICE": PASO_HELICE},
        {"CANTIDAD_VUELTAS_HELICE": CANTIDAD_VUELTAS_HELICE},
        {"PASO_EN_Y": PASO_EN_Y},
        {"DIFERENCIA": DIFERENCIA},
        {"DESFASAJE": DESFASAJE},
        {"angulos_cara_a": angulos_cara_a},
        {"angulos_cara_b_arriba": angulos_cara_b_arriba},
        {"angulos_cara_b_abajo": angulos_cara_b_abajo},
        {"vector_X_cara_a": vector_X_cara_a},
        {"vector_X_cara_b_arriba": vector_X_cara_b_arriba},
        {"vector_X_cara_b_abajo": vector_X_cara_b_abajo},
        {"L_retorno": L_retorno},
        {"TITA_retorno": TITA_retorno},
        {"DWELL_3": DWELL_3},
        {"DWELL_8": DWELL_8}
    ]
    
    diccionario_capa["calculos_iniciales"] = calculos_iniciales

    # Leer datos existentes del archivo si existe
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as json_file:
                datos_existentes = json.load(json_file)
        except Exception as e:
            print(f"Error al leer el archivo JSON existente: {e}")
            datos_existentes = {}
    else:
        datos_existentes = {}

    # Actualizar el diccionario con nuevos cálculos
    datos_existentes["calculos_iniciales"] = calculos_iniciales

    # Escribir el diccionario actualizado en el archivo JSON
    try:
        with open(filename, 'w') as json_file:
            json.dump(datos_existentes, json_file, indent=4)
        print(f"Archivo JSON '{filename}' actualizado exitosamente.")
    except Exception as e:
        print(f"Error al escribir el archivo JSON: {e}")



def generar_patrones(diccionario_capa):
    """
    Genera los patrones y listas de patrones.
    
    Args:
        diccionario_capa: Diccionario con los parámetros de la capa
    
    Returns:
        tuple: (patrones, listas_de_patrones)
    """
    patrones = vinodradov(diccionario_capa)
    listas_de_patrones = [
        obteniendo_orden_del_patron(diccionario_capa["NP"], patron[3])
        for patron in patrones
    ]
    diccionario_capa["listas_de_patrones"] = listas_de_patrones
    diccionario_capa["patrones"] = patrones
    
    # Obtener el nombre del archivo
    filename = diccionario_capa["filename"]
    
    # Leer datos existentes del archivo si existe
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as json_file:
                datos_existentes = json.load(json_file)
        except Exception as e:
            print(f"Error al leer el archivo JSON existente: {e}")
            datos_existentes = {}
    else:
        datos_existentes = {}

    # Actualizar el diccionario con nuevos cálculos
    datos_existentes["lista_de_patrones"] = listas_de_patrones
    datos_existentes["patrones"] = patrones

    # Escribir el diccionario actualizado en el archivo JSON
    try:
        with open(filename, 'w') as json_file:
            json.dump(datos_existentes, json_file, indent=4)
        print(f"Archivo JSON '{filename}' actualizado exitosamente.")
    except Exception as e:
        print(f"Error al escribir el archivo JSON: {e}")
    
    return patrones, listas_de_patrones


def graficar_patron_elegido_func(diccionario_capa, guardar_grafico):
    """Wrapper para graficar el patrón elegido."""
    grafico_patron_elegido(diccionario_capa, guardar_grafico)


def generar_puntos_codigo_g_func(diccionario_capa):
    """Wrapper para generar los puntos del código G."""
    puntos_codigo_g(diccionario_capa)


def seleccionar_patron(diccionario_capa, patrones, listas_de_patrones, parametro=None):
    """
    Selecciona un patrón y actualiza el diccionario.
    
    Args:
        diccionario_capa: Diccionario con los parámetros de la capa
        patrones: Lista de patrones
        listas_de_patrones: Lista de listas de patrones
        parametro: Número del patrón a elegir (None para usar el patrón por defecto)
    
    Returns:
        list: Lista con la información del patrón elegido
    """
    if parametro is None:
        # Si no se proporciona un parámetro, calcula el patrón elegido por defecto
        patron_elegido = 1 + min(enumerate(patrones), key=lambda x: abs(x[1][4]))[0]
    else:
        # Si se proporciona un parámetro, úsalo como el patrón elegido
        patron_elegido = parametro

    # Obtiene el orden de patrones basado en el patrón elegido
    orden_de_patrones = listas_de_patrones[patron_elegido - 1]

    # Actualiza el diccionario con la información del patrón elegido
    diccionario_capa.update({
        "patron_elegido_Nº": patron_elegido,
        "orden_del_patron_elegido": orden_de_patrones,
        "PTR": patrones[patron_elegido - 1][1],
        "Paso": patrones[patron_elegido - 1][3],
        "Dcco": patrones[patron_elegido - 1][4]
    })
    
    # Crear la lista de cálculos iniciales
    patron_info = [
        {"patron_elegido_Numero": patron_elegido},
        {"orden_del_patron_elegido": orden_de_patrones},
        {"PTR": patrones[patron_elegido - 1][1]},
        {"Paso": patrones[patron_elegido - 1][3]},
        {"Dcco": patrones[patron_elegido - 1][4]}
    ]
    
    # Obtener el nombre del archivo
    filename = diccionario_capa["filename"]
    # Leer datos existentes del archivo si existe
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as json_file:
                datos_existentes = json.load(json_file)
        except Exception as e:
            print(f"Error al leer el archivo JSON existente: {e}")
            datos_existentes = {}
    else:
        datos_existentes = {}

    # Actualizar el diccionario con nuevos cálculos
    datos_existentes["patron_elegido"] = patron_info

    # Escribir el diccionario actualizado en el archivo JSON
    try:
        with open(filename, 'w') as json_file:
            json.dump(datos_existentes, json_file, indent=4)
        print(f"Archivo JSON '{filename}' actualizado exitosamente.")
    except Exception as e:
        print(f"Error al escribir el archivo JSON: {e}")
    
    return patron_info


def insertar_en_sqlite3(diccionario_capa, usuario, nombre):
    """
    Inserta los datos de la capa en la base de datos SQLite3.
    
    Args:
        diccionario_capa: Diccionario con los parámetros de la capa
        usuario: Nombre del usuario
        nombre: Nombre de la capa
    """
    filename2 = diccionario_capa["filename2"]
    diametro_mandril = diccionario_capa["diametro_mandril"]
    longitud_util = diccionario_capa["longitud_util"]
    espesor = diccionario_capa["espesor"]
    coeficiente_rozamiento = diccionario_capa["coeficiente_rozamiento"]
    pines = diccionario_capa["pines"]
    alfa = diccionario_capa["alfa"]
    alfa_original = diccionario_capa["alfa_original"]
    ancho = diccionario_capa["ancho"]
    exceso_de_resina = diccionario_capa["exceso_de_resina"]
    corregir_angulo = diccionario_capa["corregir_angulo"]
    velocidad_de_alimentacion = diccionario_capa["velocidad_de_alimentacion"]
    alfa_corregido = diccionario_capa["calculos_iniciales"][1]["alfa_corregido"]
    ancho_eff = diccionario_capa["calculos_iniciales"][2]["ancho_eff"]
    NP = diccionario_capa["calculos_iniciales"][4]["NP"]
    patron_elegido = diccionario_capa["patron_elegido_Nº"]
    orden_del_patron_elegido = diccionario_capa["orden_del_patron_elegido"]
    PTR = diccionario_capa["PTR"]
    Paso = diccionario_capa["Paso"]
    Dcco = diccionario_capa["Dcco"]
    puntos_codigo_g_centrados = diccionario_capa["puntos_codigo_g"]
    
    # Conectar a la base de datos (la base de datos se creará si no existe)
    conn = sqlite3.connect('capas.db')
    # Crear un cursor
    cursor = conn.cursor()
    cursor.execute(''' INSERT INTO capas (
    usuario,
    nombre,
    filename2,
    diametro_mandril,
    longitud_util,
    espesor,
    coeficiente_rozamiento,
    pines,
    alfa_original,
    ancho,
    exceso_de_resina,
    corregir_angulo,
    velocidad_de_alimentacion,
    alfa_corregido,
    ancho_eff,
    NP,
    patron_elegido,
    orden_del_patron_elegido,
    PTR,
    Paso,
    Dcco,
    puntos_codigo_g
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', (
    usuario,
    nombre,
    filename2,
    diametro_mandril,
    longitud_util,
    espesor,
    coeficiente_rozamiento,
    pines,
    alfa_original,
    ancho,
    exceso_de_resina,
    corregir_angulo,
    velocidad_de_alimentacion,
    alfa_corregido,
    ancho_eff,
    NP,
    patron_elegido,
    str(orden_del_patron_elegido),
    PTR,
    Paso,
    Dcco,
    str(puntos_codigo_g_centrados)
    ))
    conn.commit()
    conn.close()


# ============================================================================
# FUNCIONES IMPLEMENTADAS (sin importaciones externas)
# ============================================================================

def calculos_iniciales(diccionario_capa):
    """Calcula los parámetros iniciales de la capa."""
    PI = diccionario_capa["PI"]
    diametro_mandril = diccionario_capa["diametro_mandril"]
    alfa = diccionario_capa["alfa"]
    ancho = diccionario_capa["ancho"]
    exceso_de_resina = diccionario_capa["exceso_de_resina"]
    corregir_angulo = diccionario_capa["corregir_angulo"]
    pines = diccionario_capa["pines"]
    
    if pines == True:
        longitud_util = diccionario_capa["longitud_util"] + 20
        coeficiente_rozamiento = 5
    else:
        longitud_util = diccionario_capa["longitud_util"]
        coeficiente_rozamiento = diccionario_capa["coeficiente_rozamiento"]
    
    alfa = math.radians(alfa)
    ancho_eff = ancho / math.cos(alfa)
    radio = diametro_mandril / 2
    
    if corregir_angulo == False and exceso_de_resina == False:
        NP = math.ceil(2 * PI * radio / ancho_eff)
    if corregir_angulo == False and exceso_de_resina == True:
        NP = math.floor(2 * PI * radio / ancho_eff)
    if corregir_angulo == True and exceso_de_resina == False:
        NP = 2 * PI * radio / ancho_eff
        NP_floor = math.floor(2 * PI * radio / ancho_eff)
        NP_ceil = math.ceil(2 * PI * radio / ancho_eff)
        if (NP_ceil - NP) < (NP - NP_floor):
            ancho_eff = (2 * PI * radio) / NP_ceil
            NP = NP_ceil
        else:
            ancho_eff = (2 * PI * radio) / NP_floor
            NP = NP_floor
        alfa = math.acos(ancho / ancho_eff)
    if corregir_angulo == True and exceso_de_resina == True:
        NP = 1 / 0
    
    DELTA = 2 * PI / NP
    PASO_HELICE = 2 * PI * radio / math.tan(alfa)
    PASO_EN_Y = PASO_HELICE / NP
    CANTIDAD_VUELTAS_HELICE = math.floor(longitud_util / PASO_HELICE)
    
    if CANTIDAD_VUELTAS_HELICE > 0:
        DIFERENCIA = longitud_util - PASO_HELICE * CANTIDAD_VUELTAS_HELICE
    else:
        DIFERENCIA = longitud_util - PASO_HELICE
    
    DESFASAJE = DIFERENCIA * math.tan(alfa) / radio
    
    vector_X_cara_a = []
    angulos_cara_a = []
    contador_a = 0
    for i in range(0, NP):
        angulos_cara_a.append(contador_a)
        vector_X_cara_a.append(contador_a * radio)
        contador_a = contador_a + DELTA
    
    vector_X_cara_b_arriba = []
    angulos_cara_b_arriba = []
    contador_b_arriba = DESFASAJE
    for j in range(0, NP):
        angulos_cara_b_arriba.append(contador_b_arriba)
        vector_X_cara_b_arriba.append(contador_b_arriba * radio)
        contador_b_arriba = contador_b_arriba + DELTA
        if contador_b_arriba > 2 * PI:
            contador_b_arriba = contador_b_arriba - 2 * PI
    
    vector_X_cara_b_abajo = []
    angulos_cara_b_abajo = []
    contador_b_abajo = 2 * PI - DESFASAJE
    for j in range(0, NP):
        angulos_cara_b_abajo.append(contador_b_abajo)
        vector_X_cara_b_abajo.append(contador_b_abajo * radio)
        contador_b_abajo = contador_b_abajo + DELTA
        if contador_b_abajo > 2 * PI:
            contador_b_abajo = contador_b_abajo - 2 * PI

    L_retorno = (radio / coeficiente_rozamiento) * (1 - (math.sin(alfa)) ** 2) / ((math.sin(alfa)) * ((1 - (math.sin(alfa)) ** 2) ** 0.5))
    TITA_retorno = (1 / coeficiente_rozamiento) * (math.log(math.sin(alfa) / (1 - ((1 - (math.sin(alfa)) ** 2) ** 0.5))))
    
    if CANTIDAD_VUELTAS_HELICE > 0:
        DIFERENCIA2 = longitud_util - PASO_HELICE * CANTIDAD_VUELTAS_HELICE
    else:
        DIFERENCIA2 = longitud_util
    
    k0 = DIFERENCIA2 * math.tan(alfa)
    k1 = k0 + TITA_retorno
    k2 = -k0 - TITA_retorno
    while k2 < k1:
        k2 = k2 + 2 * PI
    DWELL_3 = k2 - k1
    k3 = TITA_retorno
    k4 = -TITA_retorno
    while k4 < k3:
        k4 = k4 + 2 * PI
    DWELL_8 = k4 - k3

    diccionario_capa["alfa"] = alfa
    diccionario_capa["alfa_corregido"] = alfa * 180 / PI
    diccionario_capa["ancho_eff"] = ancho_eff
    diccionario_capa["radio"] = radio
    diccionario_capa["NP"] = NP
    diccionario_capa["DELTA"] = DELTA
    diccionario_capa["PASO_HELICE"] = PASO_HELICE
    diccionario_capa["CANTIDAD_VUELTAS_HELICE"] = CANTIDAD_VUELTAS_HELICE
    diccionario_capa["PASO_EN_Y"] = PASO_EN_Y
    diccionario_capa["DIFERENCIA"] = DIFERENCIA
    diccionario_capa["DESFASAJE"] = DESFASAJE
    diccionario_capa["angulos_cara_a"] = angulos_cara_a
    diccionario_capa["angulos_cara_b_arriba"] = angulos_cara_b_arriba
    diccionario_capa["angulos_cara_b_abajo"] = angulos_cara_b_abajo
    diccionario_capa["vector_X_cara_a"] = vector_X_cara_a
    diccionario_capa["vector_X_cara_b_arriba"] = vector_X_cara_b_arriba
    diccionario_capa["vector_X_cara_b_abajo"] = vector_X_cara_b_abajo
    diccionario_capa["L_retorno"] = L_retorno
    diccionario_capa["TITA_retorno"] = TITA_retorno
    diccionario_capa["DWELL_3"] = DWELL_3
    diccionario_capa["DWELL_8"] = DWELL_8
    
    filename = diccionario_capa["filename"]
    
    calculos_iniciales_list = [
        {"alfa": alfa},
        {"alfa_corregido": alfa * 180 / PI},
        {"ancho_eff": ancho_eff},
        {"radio": radio},
        {"NP": NP},
        {"DELTA": DELTA},
        {"PASO_HELICE": PASO_HELICE},
        {"CANTIDAD_VUELTAS_HELICE": CANTIDAD_VUELTAS_HELICE},
        {"PASO_EN_Y": PASO_EN_Y},
        {"DIFERENCIA": DIFERENCIA},
        {"DESFASAJE": DESFASAJE},
        {"angulos_cara_a": angulos_cara_a},
        {"angulos_cara_b_arriba": angulos_cara_b_arriba},
        {"angulos_cara_b_abajo": angulos_cara_b_abajo},
        {"vector_X_cara_a": vector_X_cara_a},
        {"vector_X_cara_b_arriba": vector_X_cara_b_arriba},
        {"vector_X_cara_b_abajo": vector_X_cara_b_abajo},
        {"L_retorno": L_retorno},
        {"TITA_retorno": TITA_retorno},
        {"DWELL_3": DWELL_3},
        {"DWELL_8": DWELL_8}
    ]
    
    diccionario_capa["calculos_iniciales"] = calculos_iniciales_list

    if os.path.exists(filename):
        try:
            with open(filename, 'r') as json_file:
                datos_existentes = json.load(json_file)
        except Exception as e:
            print(f"Error al leer el archivo JSON existente: {e}")
            datos_existentes = {}
    else:
        datos_existentes = {}

    datos_existentes["calculos_iniciales"] = calculos_iniciales_list

    try:
        with open(filename, 'w') as json_file:
            json.dump(datos_existentes, json_file, indent=4)
        print(f"Archivo JSON '{filename}' actualizado exitosamente.")
    except Exception as e:
        print(f"Error al escribir el archivo JSON: {e}")


def vinodradov(diccionario_capa):
    """Genera los patrones posibles usando el algoritmo de Vinogradov."""
    NP = diccionario_capa["NP"]
    divisores = []
    for i in range(1, NP + 1):
        if NP % i == 0:
            divisores.append(i)
    
    numeros_excluidos = [i for i in range(1, NP + 1) if i not in divisores]
    PTR = []
    a = []
    b = []
    Dcco = []
    
    PTR.append(1)
    a.append(1)
    b.append(NP - 1)
    Dcco.append(1 / (2 * 1))

    for numeros_excluido in numeros_excluidos:
        A = [NP, numeros_excluido]
        B = [0, 0]
        C = [1, 0]
        D = [0, 1]
        E = [0, 1]

        contador = 2
        while A[contador - 1] > 0:
            A.append(A[contador - 2] % A[contador - 1])
            contador = contador + 1
        A.append(0)
        
        if A[contador - 2] == 1:
            for j in range(2, contador):
                B.append(int(A[j - 2] / A[j - 1]))
                C.append(B[j] * C[j - 1] + C[j - 2])
                D.append(B[j] * D[j - 1] + D[j - 2])
                E.append(-E[j - 1])
            
            if D[contador - 2] not in b:
                if A[1] > (NP / 2):
                    dcco = 1 / (2 * (A[1] - NP))
                    PTR.append(A[1] - NP)
                    Dcco.append(dcco)
                else:
                    dcco = 1 / (2 * (A[1]))
                    PTR.append(A[1])
                    Dcco.append(dcco)
                a.append(C[contador - 2])
                b.append(D[contador - 2])
    
    patrones_posibles = []
    for ptr, val_a, val_b, dcco in zip(PTR, a, b, Dcco):
        patrones_posibles.append([NP, ptr, val_a, val_b, dcco])
    
    patrones_posibles.sort(key=lambda x: x[1])
    diccionario_capa["patrones_posibles"] = patrones_posibles
    return patrones_posibles


def obteniendo_orden_del_patron(NP, paso):
    """Obtiene el orden del patrón basado en NP y paso."""
    variable = 1
    patron = []
    while len(patron) < NP:
        patron.append(variable)
        variable = variable + paso
        if variable > NP:
            variable = variable - NP
    return patron


def areas_patron(N):
    """Genera las áreas para un patrón."""
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
        kx = k
        ky = N - 1 - k
        areas_x.append([y0[kx], yN[kx], yN[kx + 1], y0[kx + 1]])
        areas_y.append([x0[ky], x0[ky + 1], xN[ky + 1], xN[ky]])
    
    return areas_x, areas_y


def orden_de_listas_areas(N, ORDEN):
    """Obtiene el orden de las listas de áreas."""
    areas_x, areas_y = areas_patron(N)
    lista_areas = []
    
    for i in range(len(ORDEN)):
        lista_areas.append(areas_y[ORDEN[i] - 1])
        lista_areas.append(areas_x[ORDEN[i] - 1])
    
    return lista_areas


def dibujar_area(puntos, ax, color, N):
    """Dibuja un área en el gráfico."""
    x, y = zip(*puntos)
    ax.fill(x, y, color, edgecolor='black')
    ax.set_xlim(0, N)
    ax.set_ylim(0, N)


def graficar_multiples_areas(lista_de_areas, N, paso, index2, orden, ptr, Dcco, diccionario_capa, guardar_grafico, graficar_solo_esquemas):
    """Grafica múltiples áreas."""
    diametro_mandril = diccionario_capa["diametro_mandril"]
    ancho = diccionario_capa["ancho"]
    uuid_6 = diccionario_capa["uuid_6"]
    longitud_util = diccionario_capa["longitud_util"]
    alfa = diccionario_capa["alfa_original"]
    NP = diccionario_capa["NP"]
    
    fig, ax = plt.subplots()
    for index, puntos in enumerate(lista_de_areas):
        if index % 2 == 0:
            dibujar_area(puntos, ax, 'blue', N)
        else:
            dibujar_area(puntos, ax, 'red', N)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    
    lineas_orden = [orden[i:i + 20] for i in range(0, len(orden), 20)]
    texto_orden = "\n".join([", ".join(map(str, linea)) for linea in lineas_orden])
    
    ax.set_title(f"Patrón Nº {index2+1}; NP = {N}; paso = {paso}; Ptr = {ptr}; Dcco = {Dcco}")
    ax.text(
        0.5, -0.2,
        f"Orden de los patrones:\n[{texto_orden}]",
        ha='center', va='top', transform=ax.transAxes,
        fontsize=10
    )
    plt.subplots_adjust(bottom=0.2)
    
    if graficar_solo_esquemas == True:
        nombre_archivo = f"imagenes/patrones/NP={NP}_esquema_patron_Nº_{index2}_.png"
    else:
        nombre_archivo = f"imagenes/diam_{diametro_mandril}_long={longitud_util}_ancho={ancho}_alfa={alfa}_{uuid_6}_NP={NP}_esquema_patron_Nº_{index2+1}_.png"
    
    if guardar_grafico:
        plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
    
    plt.show()


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



def puntos_codigo_g(diccionario_capa):
    """Genera los puntos del código G."""
    PI = diccionario_capa["PI"]
    longitud_util = diccionario_capa["longitud_util"]
    alfa = diccionario_capa["alfa"]
    NP = diccionario_capa["NP"]
    L_retorno = diccionario_capa["L_retorno"]
    TITA_retorno = diccionario_capa["TITA_retorno"]
    DWELL_3 = diccionario_capa["DWELL_3"]
    radio = diccionario_capa["radio"]
    angulos_cara_a = diccionario_capa["angulos_cara_a"]
    angulos_cara_b_arriba = diccionario_capa["angulos_cara_b_arriba"]
    angulos_cara_b_abajo = diccionario_capa["angulos_cara_b_abajo"]

    puntos_codigo_g_array = np.zeros((NP * 8 + 1, 4))
    orden_del_patron_elegido = diccionario_capa["orden_del_patron_elegido"]
    
    angulos_cara_a_ordenado = np.zeros(NP)
    angulos_cara_b_arriba_ordenado = np.zeros(NP)
    angulos_cara_b_abajo_ordenado = np.zeros(NP)
    for k in range(len(orden_del_patron_elegido)):
        indice = orden_del_patron_elegido[k] - 1
        angulos_cara_a_ordenado[k] = angulos_cara_a[indice]
        angulos_cara_b_arriba_ordenado[k] = angulos_cara_b_arriba[indice]
        angulos_cara_b_abajo_ordenado[k] = angulos_cara_b_abajo[indice]

    CENTRADO_EN_Y = L_retorno / 2 + longitud_util / 2
    
    XX = 2 * PI
    YY = L_retorno - CENTRADO_EN_Y
    AA = 0
    FF100 = diccionario_capa["velocidad_de_alimentacion"]
    FF80 = 0.8 * diccionario_capa["velocidad_de_alimentacion"]
    FF50 = 0.5 * diccionario_capa["velocidad_de_alimentacion"]
    cara_A_primer_cuadrante = np.zeros(NP)
    cara_B_ida_primer_cuadrante = np.zeros(NP)
    cara_B_vuelta_primer_cuadrante = np.zeros(NP)
    puntos_codigo_g_array[0, :] = [XX, YY, AA, FF80]
    index = 0
    
    for i in range(NP):
        for j in range(8):
            if j == 0:
                cara_A_primer_cuadrante[i] = XX - (math.floor(XX / (2 * PI))) * 2 * PI
                XX = XX + longitud_util * math.tan(alfa) / radio
                YY = L_retorno + longitud_util - CENTRADO_EN_Y
                AA = alfa
                FF = FF100
            if j == 1:
                cara_B_ida_primer_cuadrante[i] = XX - (math.floor(XX / (2 * PI))) * 2 * PI
                XX = XX + TITA_retorno
                YY = L_retorno + longitud_util + L_retorno - CENTRADO_EN_Y
                AA = 0
                FF = FF80
            if j == 2:
                XXXX = math.ceil(XX / (2 * PI))
                DWELL_4 = XXXX * 2 * PI - XX
                XX = XX + DWELL_4
                YY = L_retorno + longitud_util + L_retorno - CENTRADO_EN_Y
                AA = 0
                FF = FF50
            if j == 3:
                if TITA_retorno > angulos_cara_b_abajo_ordenado[i]:
                    XX = XX + 2 * PI + angulos_cara_b_abajo_ordenado[i]
                else:
                    XX = XX + angulos_cara_b_abajo_ordenado[i]
                YY = L_retorno + longitud_util - CENTRADO_EN_Y
                AA = -alfa
                FF = FF80
            if j == 4:
                cara_B_vuelta_primer_cuadrante[i] = XX - (math.floor(XX / (2 * PI))) * 2 * PI
                XX = XX + longitud_util * math.tan(alfa) / radio
                YY = L_retorno - CENTRADO_EN_Y
                AA = -alfa
                FF = FF100
            if j == 5:
                XX = XX + TITA_retorno
                YY = -CENTRADO_EN_Y
                AA = 0
                FF = FF80
            if j == 6:
                XXX = math.ceil(XX / (2 * PI))
                DWELL_7 = XXX * 2 * PI - XX
                XX = XX + DWELL_7
                YY = -CENTRADO_EN_Y
                AA = 0
                FF = FF50
            if j == 7 and i < NP - 1:
                if TITA_retorno > angulos_cara_a_ordenado[i + 1]:
                    XX = XX + 2 * PI + angulos_cara_a_ordenado[i + 1]
                else:
                    XX = XX + angulos_cara_a_ordenado[i + 1]
                YY = L_retorno - CENTRADO_EN_Y
                AA = alfa
                FF = FF80
            if j == 7 and i == NP - 1:
                pass
            puntos_codigo_g_array[index + 1, :] = [XX, YY, AA, FF]
            index = index + 1

    diccionario_capa["puntos_codigo_g"] = puntos_codigo_g_array
    
    filename = diccionario_capa["filename"]
    
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as json_file:
                datos_existentes = json.load(json_file)
        except Exception as e:
            print(f"Error al leer el archivo JSON existente: {e}")
            datos_existentes = {}
    else:
        datos_existentes = {}

    datos_existentes["puntos_codigo_g"] = puntos_codigo_g_array.tolist()

    try:
        with open(filename, 'w') as json_file:
            json.dump(datos_existentes, json_file, indent=4)
        print(f"Archivo JSON '{filename}' actualizado exitosamente.")
    except Exception as e:
        print(f"Error al escribir el archivo JSON: {e}")


def _get_capa_dict(capa_item):
    """
    Helper function to extract the dictionary from either:
    - An object with 'diccionario_capa' attribute (like GeneradorPatrones instances)
    - A plain dictionary
    
    Args:
        capa_item: Either an object with diccionario_capa attribute or a dictionary
        
    Returns:
        The dictionary containing the capa data
    """
    if hasattr(capa_item, 'diccionario_capa'):
        return capa_item.diccionario_capa
    else:
        return capa_item


def txt_G_code(diccionario_capa):
    """Genera el archivo de texto con el código G."""
    PI = diccionario_capa["PI"]
    diametro_mandril = diccionario_capa["diametro_mandril"]
    longitud_util = diccionario_capa["longitud_util"]
    alfa = diccionario_capa["alfa"]
    ancho = diccionario_capa["ancho"]
    patron_elegido = diccionario_capa["patron_elegido_Nº"]
    puntos_codigoG = diccionario_capa["puntos_codigo_g"]
    
    alfa_gra = alfa * 180 / PI
    nombre_archivo = f"diam={diametro_mandril}_long={longitud_util}_ang={alfa_gra}_ancho={ancho}_patron={patron_elegido}.txt"
    num_filas = puntos_codigoG.shape[0]
    
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(f"(Código G generado por Gustavo Francisco Eichhorn)\n")
        archivo.write(f"(Diámetro del mandril: {diametro_mandril} mm)\n")
        archivo.write(f"(Longitud del mandril: {longitud_util} mm)\n")
        archivo.write(f"(Ángulo:{alfa_gra}º)\n")
        archivo.write(f"(Ancho: {ancho} mm)\n")
        archivo.write(f"(Patrón elegido: Nº {patron_elegido})\n")
        archivo.write(f"N0000 G00 X 0 Y 0 A 0 \n")
        for i in range(num_filas):
            X = puntos_codigoG[i][0]
            Y = puntos_codigoG[i][1]
            A = puntos_codigoG[i][2]
            F = puntos_codigoG[i][3]
            num_linea = str(i + 1)
            if (i + 1) < 9:
                N = f"N000{num_linea}"
            if 9 < (i + 1) < 99:
                N = f"N00{num_linea}"
            if 99 < (i + 1) < 999:
                N = f"N0{num_linea}"
            if 999 < (i + 1) < 9999:
                N = f"N{num_linea}"
            archivo.write(f"{N} G01 X {X:.2f} Y {Y:.2f} A {A:.2f} F {F:.2f}\n")


def txt_G_code(lista_de_capas, nombre_del_estudio):
    diccionario_codigo_G={}

    PI=math.pi
    numero_de_capas = len(lista_de_capas)
    matriz_general_de_capas=np.empty((0, 4), int)
    matriz_general_de_capas2=[]

    #Corrimeintos del 0 en el eje Y
    maximos=[]
    if numero_de_capas>1:
        for j in range(numero_de_capas):
            capa_dict = _get_capa_dict(lista_de_capas[j])
            puntos_codigo_gmax = capa_dict["puntos_codigo_g"] #Defino g1
            maximos.append(puntos_codigo_gmax[2][1]) #Añado el maximo al vector maximos
    else:
        capa_dict = _get_capa_dict(lista_de_capas[0])
        puntos_codigo_gmax = capa_dict["puntos_codigo_g"] #Defino g1
        maximos.append(puntos_codigo_gmax[2][1]) #Añado el maximo al vector maximos
    angulos=[]
    tamanios=[]
    tamanios_2=[]
    if numero_de_capas > 1:
        maximos_en_Y_2 = []
        for k in range(numero_de_capas):
            puntos_codigo_g0 = []
            puntos_codigo_g0_centrado = []
            capa_dict = _get_capa_dict(lista_de_capas[k])
            puntos_codigo_g0 = capa_dict["puntos_codigo_g"] #Defino g0
            puntos_codigo_g0_centrado, maximo_en_Y_2 = centrar_en_Y_puntos_codigo_g(np.array(puntos_codigo_g0))
            matriz_general_de_capas2.append(puntos_codigo_g0_centrado.tolist())
            maximos_en_Y_2.append(maximo_en_Y_2)
            tamanio=len(capa_dict["puntos_codigo_g"])
            tamanios_2.append(tamanio)
        
        #Define el nombre del archivo JSON
        with open('tamanios_2.json', 'w') as json_file:
                json.dump(tamanios_2, json_file, indent=4)
        

        #Define el nombre del archivo JSON
        with open('matriz_general_de_capas_2.json', 'w') as json_file:
                json.dump(matriz_general_de_capas2, json_file, indent=4)
        
        maximo=max(maximos_en_Y_2)

        puntos_codigo_g1 = []
        puntos_codigo_g2 = []
        puntos_codigo_g1_lista = []
        puntos_codigo_g2_lista = []

        for i in range(0, numero_de_capas):

            puntos_codigo_g1 = matriz_general_de_capas2[i] #Defino g1

            puntos_codigo_g2 = matriz_general_de_capas2[i] #Defino g2

            # Convierte la matriz a una lista para que sea serializable a JSON
            puntos_codigo_g1_lista = puntos_codigo_g1 #Matriz con los puntos para la capa individual
            

            # Guarda la variable puntos_codigo_g1 en un archivo JSON
            with open(f"puntos_codigo_g1_capa_{i+1}_(centrada).json", 'w') as json_file:
                json.dump(puntos_codigo_g1_lista, json_file, indent=4)

            #print(f"Capa {i+1}")
            #print("puntos_codigo_g0")
            #print(puntos_codigo_g0)
            capa_dict = _get_capa_dict(lista_de_capas[i])
            angulo = capa_dict["alfa_corregido"]
            angulos.append(angulo)
            tamanio=len(capa_dict["puntos_codigo_g"])
            tamanios.append(tamanio)
            # Obtener puntos_codigo_g0 originales para esta capa
            puntos_codigo_g0 = capa_dict["puntos_codigo_g"]
            adicion=0
            for k in range(tamanio):
                if k == 0:
                    puntos_codigo_g2[k][0] = puntos_codigo_g1[k][0] + 4*PI
                else:
                    puntos_codigo_g2[k][0] = puntos_codigo_g1[k][0] + adicion
                puntos_codigo_g2[k][1] = puntos_codigo_g0[k][1] + maximo
            
            #puntos_codigo_g1_lista = puntos_codigo_g1 #Matriz con los puntos para la capa individual
            
            #print(f"Capa {i+1}")
            #print("puntos_codigo_g1_maximos corridos")
            #print(puntos_codigo_g1)
            puntos_codigo_g2_lista = puntos_codigo_g2 #Matriz con los puntos para la capa total
            # Guarda la variable puntos_codigo_g1 en un archivo JSON
            with open(f"puntos_codigo_g2_capa_{i+1}.json", 'w') as json_file:
                json.dump(puntos_codigo_g2_lista, json_file, indent=4)

            # Hasta acá se escribe el codigo G para cada capa individualmente
            escribir_codigo_g(np.array(puntos_codigo_g2), lista_de_capas, i, angulo, tamanio, diccionario_codigo_G, nombre_del_estudio)
            
            if i < numero_de_capas-1:
                # Define la nueva fila que deseas agregar
                nueva_fila = [
                    #puntos_codigo_g1[tamanio-1][0] + 4*PI,
                    puntos_codigo_g2[-1][0] + 4*PI,
                    0,
                    puntos_codigo_g2[-1][2],
                    puntos_codigo_g2[-1][3]
                ]

                # Agrega la nueva fila a la matriz puntos_codigo_g1
                puntos_codigo_g2 = np.append(puntos_codigo_g2, [nueva_fila], axis=0)
                adicion = puntos_codigo_g2[-1][0] + 4*PI

            # Convierte la matriz a una lista para que sea serializable a JSON
            puntos_codigo_g2 = np.array(puntos_codigo_g2)
            puntos_codigo_g2_lista2 = puntos_codigo_g2.tolist()

            # Guarda la variable puntos_codigo_g1 en un archivo JSON
            with open(f"puntos_codigo_g2_modificado_capa_{i+1}.json", 'w') as json_file:
                json.dump(puntos_codigo_g2_lista2, json_file, indent=4)

            #print(f"Capa {i+1}")
            #print("puntos_codigo_g2 modificados")
            #print(puntos_codigo_g2)
            
            #for row in puntos_codigo_g2:
                #matriz_general_de_capas = np.append(matriz_general_de_capas, [row], axis=0)
            #print("capa multiple")
            #print("matriz_general_de_capas")
            #print(matriz_general_de_capas)
        
        matriz_general_de_capas3=[]
        with open('matriz_general_de_capas_2.json', 'r') as archivo:
            matriz_general_de_capas3 = json.load(archivo)
        #Define el nombre del archivo JSON
        with open('matriz_general_de_capas_3.json', 'w') as json_file:
                json.dump(matriz_general_de_capas3, json_file, indent=4)
        matriz_general_de_capas4=[]
        matriz_general_de_capas5=[]
        matriz_intermedia=[9,9,9,9]
        # Añade las matrices originales e intermedias a la lista final
        for ii, matriz in enumerate(matriz_general_de_capas3):
            matriz_general_de_capas4.append(matriz)
            #if ii < len(matriz_general_de_capas3) - 1:
                #matriz_intermedia=[[7,7,7,7]]
                #matriz_general_de_capas4.append(matriz_intermedia)
        with open('matriz_general_de_capas_4_original.json', 'w') as json_file:
                json.dump(matriz_general_de_capas4, json_file, indent=4)

        for jj in range(numero_de_capas):
            
            if jj%2==1:
                matriz_general_de_capas4[jj][0][0] = matriz_general_de_capas4[jj-1][-1][0] + 4*PI
                # Verificar que jj+1 no exceda el rango antes de acceder
                if jj+1 < numero_de_capas:
                    matriz_general_de_capas4[jj][0][1] = matriz_general_de_capas4[jj+1][0][1] + maximo
                else:
                    matriz_general_de_capas4[jj][0][1] = matriz_general_de_capas4[jj][0][1] + maximo
                matriz_general_de_capas4[jj][0][2] = matriz_general_de_capas4[jj-1][-1][2]
                matriz_general_de_capas4[jj][0][3] = matriz_general_de_capas4[jj-1][-1][3]
            else:
                matriz_general_de_capas4[jj][0][1] = matriz_general_de_capas4[jj][0][1] + maximo

        # Este bucle parece tener un error - kk no está definido, debería ser jj o eliminarse
        # Comentado temporalmente hasta entender su propósito
        # for mm in range(len(matriz_general_de_capas4[jj])):
        #     matriz_general_de_capas4[kk][mm][0] = matriz_general_de_capas4[kk][mm][0] + maximo
        with open('matriz_general_de_capas_4_modificacion_intermedios.json', 'w') as json_file:
                json.dump(matriz_general_de_capas4, json_file, indent=4)
        
        adicion=0
        for kk in range(0, len(matriz_general_de_capas4)):
            
            print(f"Iteración kk={kk}")
            print(f"Adición actualizada: {adicion}")
            with open('adicion.json', 'w') as json_file:
                json.dump(adicion, json_file, indent=4)
            for ll in range(len(matriz_general_de_capas4[kk])):
                matriz_general_de_capas4[kk][ll][0] = matriz_general_de_capas4[kk][ll][0] + adicion
                matriz_general_de_capas4[kk][ll][1] = matriz_general_de_capas4[kk][ll][1] + maximo
                if ll==len(matriz_general_de_capas4[kk])-1:
                    adicion = adicion + matriz_general_de_capas4[kk][ll][0]
        
        for jj in range(numero_de_capas-1):
            matriz_general_de_capas4[jj][-1][1] = matriz_general_de_capas4[jj+1][0][1]
        
        # Agrupa todas las matrices en una sola matriz
        if matriz_general_de_capas4:
            matriz_general_de_capas5 = np.vstack(matriz_general_de_capas4)
        else:
            matriz_general_de_capas5 = np.empty((0, 4))  # Asegúrate de que no esté vacío
        #Define el nombre del archivo JSON
        with open('matriz_general_de_capas_4_final.json', 'w') as json_file:
                json.dump(matriz_general_de_capas4, json_file, indent=4)
        #Define el nombre del archivo JSON
        with open('matriz_general_de_capas_5.json', 'w') as json_file:
                json.dump(matriz_general_de_capas5.tolist(), json_file, indent=4)
        matriz_general_de_capas = matriz_general_de_capas5

    else:
        capa_dict = _get_capa_dict(lista_de_capas[0])
        puntos_codigo_g1=np.array(capa_dict["puntos_codigo_g"])
        maximo=max(maximos)-maximos[0]
        puntos_codigo_g1[:,1] += maximo + maximos[0] / 2 #Le añado el maximo para correr el cero
        angulo = capa_dict["alfa_corregido"]
        angulos.append(angulo)
        tamanio=len(capa_dict["puntos_codigo_g"])
        tamanios.append(tamanio)
        for row in puntos_codigo_g1:
            matriz_general_de_capas = np.append(matriz_general_de_capas, [row], axis=0)

        escribir_codigo_g(matriz_general_de_capas, lista_de_capas, -2, angulo, tamanio, diccionario_codigo_G, nombre_del_estudio)

    #Escribo el codigo G total

    escribir_codigo_g(matriz_general_de_capas, lista_de_capas, -1, angulos, tamanios, diccionario_codigo_G, nombre_del_estudio)
    return(diccionario_codigo_G)


def centrar_en_Y_puntos_codigo_g(puntos_codigo_g):
    # Encuentra el valor mínimo en el eje Y
    puntos_array = np.array(puntos_codigo_g)
    minimo_en_Y = min(puntos_array[:,1])
    # Encuentra el valor máximo en el eje Y
    maximo_en_Y = max(puntos_array[:,1])
    # Resta el valor mínimo en el eje Y a todos los puntos
    promedio = (maximo_en_Y + minimo_en_Y) / 2
    puntos_array[:,1] -= promedio
    maximo_en_Y_2 = maximo_en_Y-promedio
    return puntos_array, maximo_en_Y_2


def escribir_codigo_g(matriz_general_de_capas, lista_de_capas, i, angulo, multiples_capas, diccionario_codigo_G, nombre_del_estudio):
    # Determinar qué capa usar según el índice i
    if i == -1 or i == -2:
        capa_index = 0  # Para Total o Capa_Unica, usar la primera capa
    else:
        capa_index = i  # Para capas individuales, usar el índice correspondiente
    
    capa_dict = _get_capa_dict(lista_de_capas[capa_index])  # Maneja tanto objetos como diccionarios
    diametro_mandril = capa_dict["diametro_mandril"]
    longitud_util = capa_dict["longitud_util"]
    ancho = capa_dict["ancho"]
    alfa = capa_dict["alfa"]
    PI = capa_dict["PI"]
    angulo = int(round(alfa * 180 / PI))  # Convertir a grados y luego a entero sin decimales
    
    lista_de_cadenas_de_texto_de_codigo_G=[]
    #print("type(diccionario_codigo_G) 1 escribir_codigo_g")
    #print(type(diccionario_codigo_G))
    # Genera un UUID y conviértelo a una cadena de texto
    ii=i
    if i==-1:
        texto=f"Total_{nombre_del_estudio}"
        #uuid_aleatorio = str(uuid.uuid4())
        #uuid_6=uuid_aleatorio[:6] # Puedes recortar a la longitud que desees si necesitas menos de 36 caracteres
        uuid_6 = capa_dict["uuid_6"]
    elif i==-2:
        texto=f"_angulo={angulo}º_Capa_Unica_{nombre_del_estudio}"
        uuid_6 = capa_dict["uuid_6"]
    else:
        texto=f"_angulo={angulo}º_Capa_{str(i+1)}_{nombre_del_estudio}"
        uuid_6 = capa_dict["uuid_6"]
    
    nombre_archivo=f"diam={diametro_mandril}_long={longitud_util}_ancho={ancho}_{texto}_{uuid_6}.txt"
    
    lista_de_cadenas_de_texto_de_codigo_G.append(nombre_archivo)
    
    num_filas = matriz_general_de_capas.shape[0]
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(f"(Codigo G generado por Gustavo Francisco Eichhorn)\n")
        lista_de_cadenas_de_texto_de_codigo_G.append(f"(Codigo G generado por Gustavo Francisco Eichhorn)")
        archivo.write(f"(Nombre del archivo: '{nombre_archivo}')\n")
        lista_de_cadenas_de_texto_de_codigo_G.append(f"(Nombre del archivo: '{nombre_archivo}')")
        archivo.write(f"(Diametro del mandril: {diametro_mandril} mm)\n")
        lista_de_cadenas_de_texto_de_codigo_G.append(f"(Diametro del mandril: {diametro_mandril} mm)")
        archivo.write(f"(Longitud del mandril: {longitud_util} mm)\n")
        lista_de_cadenas_de_texto_de_codigo_G.append(f"(Longitud del mandril: {longitud_util} mm)")
        archivo.write(f"(Ancho: {ancho} mm)\n")
        lista_de_cadenas_de_texto_de_codigo_G.append(f"(Ancho: {ancho} mm)")
        if isinstance(angulo, list):
            for k in range(len(angulo)):
                archivo.write(f"(Angulo capa {k+1}: {angulo[k]}º)\n")
                lista_de_cadenas_de_texto_de_codigo_G.append(f"(Angulo capa {k+1}: {angulo[k]}º)")
        else:
            archivo.write(f"(Angulo: {angulo}º)\n")
            lista_de_cadenas_de_texto_de_codigo_G.append(f"(Angulo: {angulo}º)")
        if isinstance(multiples_capas, list):
            linea=7
            for j in range(len(multiples_capas)):
                archivo.write(f"(La capa {j+1} empieza en la linea: {linea})\n")
                lista_de_cadenas_de_texto_de_codigo_G.append(f"(La capa {j+1} empieza en la linea: {linea})")
                linea=linea+multiples_capas[j]+2
        else:
            archivo.write(f"(Cantidad de lineas del codigo G: {multiples_capas+9})\n")
            lista_de_cadenas_de_texto_de_codigo_G.append(f"(Cantidad de lineas del codigo G: {multiples_capas+7})")
        archivo.write(f"N 0000 G00 X 0 Y 0 A 0 \n")
        lista_de_cadenas_de_texto_de_codigo_G.append(f"N 0000 G00 X 0 Y 0 A 0")
        for i in range(num_filas):
            X=matriz_general_de_capas[i][0]
            Y=matriz_general_de_capas[i][1]
            A=matriz_general_de_capas[i][2]
            F=matriz_general_de_capas[i][3]
            num_linea=str(i+1)
            if (i+1)<9:
                N=f"N 0000{num_linea}"
            if 9<(i+1)<99:
                N=f"N 000{num_linea}"
            if 99<(i+1)<999:
                N=f"N 00{num_linea}"
            if 999<(i+1)<9999:
                N=f"N 0{num_linea}"
            if 9999<(i+1):
                N=f"N {num_linea}"
            # Escribir línea con valores de X, Y, A y F formateados a dos decimales
            archivo.write(f"{N} G01 X {X:.2f} Y {Y:.2f} A {A:.2f} F {F:.2f}\n")
            lista_de_cadenas_de_texto_de_codigo_G.append(f"{N} G01 X {X:.2f} Y {Y:.2f} A {A:.2f} F {F:.2f}")
    #print("type(diccionario_codigo_G) 2 escribir_codigo_g")
    #print(type(diccionario_codigo_G))
    #print(type(lista_de_cadenas_de_texto_de_codigo_G))
    if ii==-1:
        diccionario_codigo_G["Total"]=lista_de_cadenas_de_texto_de_codigo_G
        #print(diccionario_codigo_G["Total"])
        return(diccionario_codigo_G["Total"])
    if ii==-2:
        diccionario_codigo_G["Capa_Unica"]=lista_de_cadenas_de_texto_de_codigo_G
        #print(diccionario_codigo_G["Capa_Unica"])
        return(diccionario_codigo_G["Capa_Unica"])
    if ii!=-1 and ii!=-2:
        string=f"Capa_{str(ii+1)}"
        diccionario_codigo_G[string]=lista_de_cadenas_de_texto_de_codigo_G
        #print(diccionario_codigo_G[string])
        return(diccionario_codigo_G[string])
