import numpy as np
import math
import os
import json

def puntos_codigo_g(diccionario_capa):
    PI = diccionario_capa["PI"]
    longitud_util = diccionario_capa["longitud_util"]
    alfa = diccionario_capa["alfa"]
    NP = diccionario_capa["NP"]
    L_retorno = diccionario_capa["L_retorno"]
    TITA_retorno = diccionario_capa["TITA_retorno"]
    DWELL_3 = diccionario_capa["DWELL_3"]
    #patrones = diccionario_capa["patrones"]
    #patron_elegido = diccionario_capa["patron_elegido_Nº"]
    radio = diccionario_capa["radio"]
    angulos_cara_a = diccionario_capa["angulos_cara_a"]
    angulos_cara_b_arriba = diccionario_capa["angulos_cara_b_arriba"]
    angulos_cara_b_abajo = diccionario_capa["angulos_cara_b_abajo"]

    puntos_codigo_g=np.zeros((NP*8+1, 4))
    orden_del_patron_elegido = diccionario_capa["orden_del_patron_elegido"]
    
    #Reordenar
    angulos_cara_a_ordenado=np.zeros(NP)
    angulos_cara_b_arriba_ordenado=np.zeros(NP)
    angulos_cara_b_abajo_ordenado=np.zeros(NP)
    for k in range(len(orden_del_patron_elegido)):
        indice=orden_del_patron_elegido[k]-1
        angulos_cara_a_ordenado[k]=angulos_cara_a[indice]
        angulos_cara_b_arriba_ordenado[k]=angulos_cara_b_arriba[indice]
        angulos_cara_b_abajo_ordenado[k]=angulos_cara_b_abajo[indice]

    
    #paso_angular_patron=patrones[patron_elegido-1][1]
    
    #angulo_vuelta_dwell=(2*PI/NP)*(paso_angular_patron-1)
    
    CENTRADO_EN_Y=L_retorno+longitud_util/2
    
    XX=2*PI #Giro del mandril en radianes
    YY=L_retorno-CENTRADO_EN_Y #Desplazamiento del carro en mm
    AA=0 #Giro del ojal en radianes
    FF100=diccionario_capa["velocidad_de_alimentacion"] #Velocidad de alimentacion mm/min
    FF80=0.8*diccionario_capa["velocidad_de_alimentacion"] #Velocidad de alimentacion mm/min
    FF50=0.5*diccionario_capa["velocidad_de_alimentacion"] #Velocidad de alimentacion mm/min
    cara_A_primer_cuadrante=np.zeros(NP)
    cara_B_ida_primer_cuadrante=np.zeros(NP)
    cara_B_vuelta_primer_cuadrante=np.zeros(NP)
    puntos_codigo_g[0, :] = [XX, YY, AA, FF80]
    index=0
    for i in range(NP):
        for j in range(8):
            if j==0: #Zona geodesica ida
                cara_A_primer_cuadrante[i]=XX-(math.floor(XX/(2*PI)))*2*PI
                #print(XX)
                XX=XX+longitud_util*math.tan(alfa)/radio
                YY=L_retorno+longitud_util-CENTRADO_EN_Y
                AA=alfa
                FF=FF100
            if j==1: #Zona 1 de retorno ida
                cara_B_ida_primer_cuadrante[i]=XX-(math.floor(XX/(2*PI)))*2*PI
                XX=XX+TITA_retorno
                YY=L_retorno+longitud_util+L_retorno-CENTRADO_EN_Y
                AA=0
                FF=FF80
            if j==2: #Zona 2 de retorno ida
                XXXX=math.ceil(XX/(2*PI))
                DWELL_4=XXXX*2*PI-XX
                XX=XX+DWELL_4 #Queda como múltiplo de 2*PI
                YY=L_retorno+longitud_util+L_retorno-CENTRADO_EN_Y
                AA=0
                FF=FF50
            if j==3: #Zona 3 de retorno ida
                if TITA_retorno > angulos_cara_b_abajo_ordenado[i]:
                    XX=XX+2*PI+angulos_cara_b_abajo_ordenado[i] #Me aseguro que no haya resbalamiento
                else:
                    XX=XX+angulos_cara_b_abajo_ordenado[i]
                YY=L_retorno+longitud_util-CENTRADO_EN_Y
                AA=-alfa
                FF=FF80
            if j==4: #Zona geodesica vuelta
                cara_B_vuelta_primer_cuadrante[i]=XX-(math.floor(XX/(2*PI)))*2*PI
                XX=XX+longitud_util*math.tan(alfa)/radio
                YY=L_retorno-CENTRADO_EN_Y
                AA=-alfa
                FF=FF100
            if j==5: #Zona 1 de retorno vuelta
                XX=XX+TITA_retorno
                YY=-CENTRADO_EN_Y
                AA=0
                FF=FF80
            if j==6: #Zona 2 de retorno vuelta
                XXX=math.ceil(XX/(2*PI))
                DWELL_7=XXX*2*PI-XX
                XX=XX+DWELL_7 #Queda en un múltiplo de 2*PI
                YY=-CENTRADO_EN_Y
                AA=0
                FF=FF50
            if j==7 and i<NP-1: #Zona 3 de retorno vuelta
                if TITA_retorno > angulos_cara_a_ordenado[i+1]:
                    XX=XX+2*PI+angulos_cara_a_ordenado[i+1] #Me aseguro que no haya resbalamiento
                else:
                    XX=XX+angulos_cara_a_ordenado[i+1]
                YY=L_retorno-CENTRADO_EN_Y
                AA=alfa
                FF=FF80
            if j==7 and i==NP-1: #Zona 3 de retorno vuelta
                pass
            puntos_codigo_g[index+1, :] = [XX, YY, AA, FF]
            index=index+1
    '''
    print("orden_del_patron_elegido")
    print(orden_del_patron_elegido)
    print("")
    print("angulos_cara_a")
    print(angulos_cara_a)
    print("angulos_cara_a_ordenado")
    print(angulos_cara_a_ordenado)
    print("cara_A_primer_cuadrante")
    print(cara_A_primer_cuadrante)
    print("")
    print("angulos_cara_b_arriba")
    print(angulos_cara_b_arriba)
    print("angulos_cara_b_arriba_ordenado")
    print(angulos_cara_b_arriba_ordenado)
    print("cara_B_ida_primer_cuadrante")
    print(cara_B_ida_primer_cuadrante)
    print("")
    print("angulos_cara_b_abajo")
    print(angulos_cara_b_abajo)
    print("angulos_cara_b_abajo_ordenado")
    print(angulos_cara_b_abajo_ordenado)
    print("cara_B_vuelta_primer_cuadrante")
    print(cara_B_vuelta_primer_cuadrante)
    '''


    diccionario_capa["puntos_codigo_g"] = puntos_codigo_g
    
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
    datos_existentes["puntos_codigo_g_centrados"] = puntos_codigo_g.tolist()

    # Escribir el diccionario actualizado en el archivo JSON
    try:
        with open(filename, 'w') as json_file:
            json.dump(datos_existentes, json_file, indent=4)
        print(f"Archivo JSON '{filename}' actualizado exitosamente.")
    except Exception as e:
        print(f"Error al escribir el archivo JSON: {e}")