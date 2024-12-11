import math
import json
import os

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


# alfa = ángulo corregido (o no) del bobinado de filamentos
# ancho_eff = ancho efectivo referido a ese ángulo alfa
# radio = radio del mandril
# NP = Número de circuitos necesario para cubrir completamente el mandril con una capa
# DELTA = Salto angular entre una pasada y otra en el circuito del devanado.
# PASO_HELICE = distancia en mm en la que la hélice gira una vuelta completa (2π)
# CANTIDAD_VUELTAS_HELICE= Cantidad entera de vueltas completas que realiza la helice en la longitud especificada
# DIFERENCIA= diferencia entre la longitud total y la longitud recorrida en vueltas que han completado un giro completo
# DESFASAJE = cuanto se desfasaja la cara B real respecto de la cara B teorica con vueltas completas
# angulos_cara_a = Conjunto de ángulos en radianes comprendidos entre [0 2π] de la cara A
# angulos_cara_b = Conjunto de ángulos en radianes comprendidos entre [0 2π] de la cara B real