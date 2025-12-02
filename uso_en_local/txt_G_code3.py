import numpy as np
import uuid
import math
import json
from escribir_codigo_g import escribir_codigo_g

def txt_G_code3(lista_de_capas, nombre_del_estudio):
    diccionario_codigo_G = {}  # Inicializa el diccionario
    numero_de_capas = len(lista_de_capas)
    if numero_de_capas > 1:
        capas_individuales(lista_de_capas, nombre_del_estudio, diccionario_codigo_G)
        capa_total(lista_de_capas, nombre_del_estudio, diccionario_codigo_G)
    else:
        capa_unica(lista_de_capas, nombre_del_estudio, diccionario_codigo_G)
    return(diccionario_codigo_G)

def capa_unica(lista_de_capas, nombre_del_estudio, diccionario_codigo_G):

    PI=math.pi
    numero_de_capas = len(lista_de_capas)
    #matriz_general_de_capas=np.empty((0, 4), int)

    # centrado
    puntos_codigo_g0 = []
    puntos_codigo_g0_centrado = []
    
    # Check if the item is an object with 'diccionario_capa' or just a dict
    if hasattr(lista_de_capas[0], 'diccionario_capa'):
        puntos_codigo_g0 = lista_de_capas[0].diccionario_capa["puntos_codigo_g"] #Defino g0
    else:
        puntos_codigo_g0 = lista_de_capas[0]["puntos_codigo_g"] #Defino g0

    puntos_codigo_g0_centrado, maximo = centrar_en_Y_puntos_codigo_g(puntos_codigo_g0)
    angulo = lista_de_capas[0].diccionario_capa["alfa_corregido"]
    tamanio=len(lista_de_capas[0].diccionario_capa["puntos_codigo_g"])

    #Corrimientos del 0 en el eje Y
    puntos_codigo_g1 = puntos_codigo_g0_centrado

    for k in range(tamanio):
        puntos_codigo_g1[k,1] = puntos_codigo_g1[k,1] + maximo #Le añado el maximo para correr el cero

    diccionario = {
        "nombre_del_estudio": nombre_del_estudio,
        "angulo": angulo,
        "tamanio": tamanio,
        "maximo": maximo,
        "puntos_codigo_g0": puntos_codigo_g0.tolist(),
        "puntos_codigo_g0_centrado": puntos_codigo_g0_centrado.tolist(),
        "puntos_codigo_g1": puntos_codigo_g1.tolist(),
    }
    with open('puntos_codigo_g_capa_unica.json', 'w') as json_file:
                json.dump(diccionario, json_file, indent=4)
    escribir_codigo_g(puntos_codigo_g1, lista_de_capas, -2, angulo, tamanio, diccionario_codigo_G, nombre_del_estudio)

def capas_individuales(lista_de_capas, nombre_del_estudio, diccionario_codigo_G):

    PI=math.pi
    numero_de_capas = len(lista_de_capas)
    matriz_general_de_capas=np.empty((0, 4), int)
    matriz_general_de_capas2=[]
    
    #Corrimeintos del 0 en el eje Y
    maximos=[]
    for j in range(numero_de_capas):
        # Check if the item is an object with 'diccionario_capa' or just a dict
        if hasattr(lista_de_capas[j], 'diccionario_capa'):
            puntos_codigo_gmax = lista_de_capas[j].diccionario_capa["puntos_codigo_g"] #Defino g1
        else:
            puntos_codigo_gmax = lista_de_capas[j]["puntos_codigo_g"] #Defino g1
        maximos.append(puntos_codigo_gmax[2][1]) #Añado el maximo al vector maximos
    angulos=[]
    tamanios=[]
    tamanios_2=[]
    if numero_de_capas > 1:
        maximos_en_Y_2 = []
        for k in range(numero_de_capas):
            puntos_codigo_g0 = []
            puntos_codigo_g0_centrado = []
            # Check if the item is an object with 'diccionario_capa' or just a dict
            if hasattr(lista_de_capas[k], 'diccionario_capa'):
                puntos_codigo_g0 = lista_de_capas[k].diccionario_capa["puntos_codigo_g"] #Defino g0
            else:
                puntos_codigo_g0 = lista_de_capas[k]["puntos_codigo_g"] #Defino g0
            puntos_codigo_g0_centrado, maximo_en_Y_2 = centrar_en_Y_puntos_codigo_g(puntos_codigo_g0)
            matriz_general_de_capas2.append(puntos_codigo_g0_centrado.tolist())
            maximos_en_Y_2.append(maximo_en_Y_2)
            tamanio=len(lista_de_capas[k].diccionario_capa["puntos_codigo_g"])
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

            # Check if the item is an object with 'diccionario_capa' or just a dict
            if hasattr(lista_de_capas[i], 'diccionario_capa'):
                angulo = lista_de_capas[i].diccionario_capa["alfa_corregido"]
                tamanio=len(lista_de_capas[i].diccionario_capa["puntos_codigo_g"])
            else:
                angulo = lista_de_capas[i]["alfa_corregido"]
                tamanio=len(lista_de_capas[i]["puntos_codigo_g"])

            angulos.append(angulo)
            tamanios.append(tamanio)
            adicion=0
            for k in range(tamanios):
                if k == 0:
                    puntos_codigo_g2[k][0] = puntos_codigo_g1[k][0] + 4*PI
                else:
                    puntos_codigo_g2[k][0] = puntos_codigo_g1[k][0] + adicion
                puntos_codigo_g2[k][1] = puntos_codigo_g0[k][1] + maximo
            
            puntos_codigo_g2_lista = puntos_codigo_g2 #Matriz con los puntos para la capa total
            # Guarda la variable puntos_codigo_g1 en un archivo JSON
            with open(f"puntos_codigo_g2_capa_{i+1}.json", 'w') as json_file:
                json.dump(puntos_codigo_g2_lista, json_file, indent=4)

            # Hasta acá se escribe el codigo G para cada capa individualmente
            escribir_codigo_g(np.array(puntos_codigo_g2), lista_de_capas, i, angulo, tamanio, diccionario_codigo_G, nombre_del_estudio)

def capa_total(lista_de_capas, nombre_del_estudio, diccionario_codigo_G):

    PI=math.pi
    numero_de_capas = len(lista_de_capas)
    matriz_general_de_capas=np.empty((0, 4), int)
    matriz_general_de_capas2=[]
    
    #Corrimeintos del 0 en el eje Y
    maximos=[]
    for j in range(numero_de_capas):
        # Check if the item is an object with 'diccionario_capa' or just a dict
        if hasattr(lista_de_capas[j], 'diccionario_capa'):
            puntos_codigo_gmax = lista_de_capas[j].diccionario_capa["puntos_codigo_g"] #Defino g1
        else:
            puntos_codigo_gmax = lista_de_capas[j]["puntos_codigo_g"] #Defino g1
        maximos.append(puntos_codigo_gmax[2][1]) #Añado el maximo al vector maximos
    
    angulos=[]
    tamanios=[]
    tamanios_2=[]
    maximos_en_Y_2 = []
    for k in range(numero_de_capas):
        puntos_codigo_g0 = []
        puntos_codigo_g0_centrado = []
        # Check if the item is an object with 'diccionario_capa' or just a dict
        if hasattr(lista_de_capas[k], 'diccionario_capa'):
            puntos_codigo_g0 = lista_de_capas[k].diccionario_capa["puntos_codigo_g"] #Defino g0
            tamanio=len(lista_de_capas[k].diccionario_capa["puntos_codigo_g"])
        else:
            puntos_codigo_g0 = lista_de_capas[k]["puntos_codigo_g"] #Defino g0
            tamanio=len(lista_de_capas[k]["puntos_codigo_g"])

        puntos_codigo_g0_centrado, maximo_en_Y_2 = centrar_en_Y_puntos_codigo_g(puntos_codigo_g0)
        matriz_general_de_capas2.append(puntos_codigo_g0_centrado.tolist())
        maximos_en_Y_2.append(maximo_en_Y_2)

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
        # Check if the item is an object with 'diccionario_capa' or just a dict
        if hasattr(lista_de_capas[i], 'diccionario_capa'):
            angulo = lista_de_capas[i].diccionario_capa["alfa_corregido"]
            tamanio=len(lista_de_capas[i].diccionario_capa["puntos_codigo_g"])
        else:
            angulo = lista_de_capas[i]["alfa_corregido"]
            tamanio=len(lista_de_capas[i]["puntos_codigo_g"])

        angulos.append(angulo)
        tamanios.append(tamanio)
        adicion=0
        for k in range(tamanios):
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
            matriz_general_de_capas4[jj][0][1] = matriz_general_de_capas4[jj+1][0][1] + maximo
            matriz_general_de_capas4[jj][0][2] = matriz_general_de_capas4[jj-1][-1][2]
            matriz_general_de_capas4[jj][0][3] = matriz_general_de_capas4[jj-1][-1][3]
        else:
            matriz_general_de_capas4[jj][0][1] = matriz_general_de_capas4[jj][0][1] + maximo

    for mm in range(len(matriz_general_de_capas4[jj])):
        matriz_general_de_capas4[kk][mm][0] = matriz_general_de_capas4[kk][mm][0] + maximo
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

def centrar_en_Y_puntos_codigo_g(puntos_codigo_g):
    # Encuentra el valor mínimo en el eje Y
    minimo_en_Y = min(puntos_codigo_g[:,1])
    # Encuentra el valor máximo en el eje Y
    maximo_en_Y = max(puntos_codigo_g[:,1])
    # Resta el valor mínimo en el eje Y a todos los puntos
    promedio = (maximo_en_Y + minimo_en_Y) / 2
    puntos_codigo_g[:,1] -= promedio
    maximo_en_Y_2 = maximo_en_Y-promedio
    return puntos_codigo_g, maximo_en_Y_2