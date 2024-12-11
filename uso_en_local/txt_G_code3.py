import numpy as np
import uuid

def txt_G_code3(lista_de_capas):
  
    diccionario_codigo_G={}
    
    PI=lista_de_capas[0].diccionario_capa["PI"]
    numero_de_capas = len(lista_de_capas)
    matriz_general_de_capas=np.empty((0, 4), int)
    
    #Corrimeintos del 0 en el eje Y
    maximos=[]
    if numero_de_capas>1:
        for j in range(numero_de_capas):
          puntos_codigo_gmax = lista_de_capas[j].diccionario_capa["puntos_codigo_g"] #Defino g1
          maximos.append(puntos_codigo_gmax[2][1]) #Añado el maximo al vector maximos
    else:
        puntos_codigo_gmax = lista_de_capas[0].diccionario_capa["puntos_codigo_g"] #Defino g1
        maximos.append(puntos_codigo_gmax[2][1]) #Añado el maximo al vector maximos
    maximo=max(maximos)
    angulos=[]
    tamanios=[]
    if numero_de_capas>1:
        
        for i in range(numero_de_capas):
            lista_de_capas[j].diccionario_capa["puntos_codigo_g"] #Defino g1
            #Defino g0
            if i>0:
                puntos_codigo_g0 = lista_de_capas[i-1].diccionario_capa["puntos_codigo_g"]
            else:
                puntos_codigo_g0 = np.array([[4*PI, 0, 0, 0]])
            
            puntos_codigo_g1 = lista_de_capas[i].diccionario_capa["puntos_codigo_g"] #Defino g1
            angulo = lista_de_capas[i].diccionario_capa["alfa_corregido"]
            angulos.append(angulo)
            tamanio=len(lista_de_capas[i].diccionario_capa["puntos_codigo_g"])
            tamanios.append(tamanio)
            
            puntos_codigo_g1[:,1] += maximo #Le añado el maximo para correr el cero
            #print(f"type(diccionario_codigo_G) capa individual {i+1}")
            #print(type(diccionario_codigo_G))
            escribir_codigo_g(puntos_codigo_g1, lista_de_capas, i, angulo, tamanio, diccionario_codigo_G)
            
            puntos_codigo_g2 = lista_de_capas[i].diccionario_capa["puntos_codigo_g"] #Defino g2
            puntos_codigo_g2[:,0] += puntos_codigo_g0[-1, 0]+4*PI #añado el ultimo angulo de g0 al vector actual g2 para añadir una capa más
            #El 4*PI me asegura dos vueltas hasta llegar a la posicion de la nueva capa
            
            for row in puntos_codigo_g2:
                matriz_general_de_capas = np.append(matriz_general_de_capas, [row], axis=0)
    else:
        puntos_codigo_g1=lista_de_capas[0].diccionario_capa["puntos_codigo_g"]
        puntos_codigo_g1[:,1] += maximo #Le añado el maximo para correr el cero
        angulo = lista_de_capas[0].diccionario_capa["alfa_corregido"]
        angulos.append(angulo)
        tamanio=len(lista_de_capas[0].diccionario_capa["puntos_codigo_g"])
        tamanios.append(tamanio)
        for row in puntos_codigo_g1:
            matriz_general_de_capas = np.append(matriz_general_de_capas, [row], axis=0)
        #print("type(diccionario_codigo_G) capa unica")
        #print(type(diccionario_codigo_G))
        escribir_codigo_g(matriz_general_de_capas, lista_de_capas, -2, angulo, tamanio, diccionario_codigo_G)
        #print("")
        #print("capa unica")
    #Escribo el codigo G total
    #print("type(diccionario_codigo_G) total")
    #print(type(diccionario_codigo_G))
    escribir_codigo_g(matriz_general_de_capas, lista_de_capas, -1, angulos, tamanios, diccionario_codigo_G)
    return(diccionario_codigo_G)

def escribir_codigo_g(matriz_general_de_capas, lista_de_capas, i, angulo, multiples_capas, diccionario_codigo_G):
    diametro_mandril = lista_de_capas[0].diccionario_capa["diametro_mandril"]
    longitud_util = lista_de_capas[0].diccionario_capa["longitud_util"]
    ancho = lista_de_capas[0].diccionario_capa["ancho"]
    
    lista_de_cadenas_de_texto_de_codigo_G=[]
    #print("type(diccionario_codigo_G) 1 escribir_codigo_g")
    #print(type(diccionario_codigo_G))
    # Genera un UUID y conviértelo a una cadena de texto
    ii=i
    if i==-1:
        texto="Total"
        #uuid_aleatorio = str(uuid.uuid4())
        #uuid_6=uuid_aleatorio[:6] # Puedes recortar a la longitud que desees si necesitas menos de 36 caracteres
        uuid_6 = lista_de_capas[0].diccionario_capa["uuid_6"]
    elif i==-2:
        texto="Capa_Unica"
        uuid_6 = lista_de_capas[0].diccionario_capa["uuid_6"]
    else:
        texto=f"Capa_{str(i+1)}"
        uuid_6 = lista_de_capas[0].diccionario_capa["uuid_6"]
    
    nombre_archivo=f"diam={diametro_mandril}_long={longitud_util}_ancho={ancho}_{texto}_{uuid_6}.txt"
    
    lista_de_cadenas_de_texto_de_codigo_G.append(nombre_archivo)
    
    num_filas = matriz_general_de_capas.shape[0]
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(f"(Codigo G generado por Gustavo Francisco Eichhorn)\n")
        lista_de_cadenas_de_texto_de_codigo_G.append(f"(Codigo G generado por Gustavo Francisco Eichhorn)")
        archivo.write(f"(Diametro del mandril: {diametro_mandril} mm)\n")
        lista_de_cadenas_de_texto_de_codigo_G.append(f"(Diametro del mandril: {diametro_mandril} mm)")
        archivo.write(f"(Longitud del mandril: {longitud_util} mm)\n")
        lista_de_cadenas_de_texto_de_codigo_G.append(f"(Longitud del mandril: {longitud_util} mm)")
        archivo.write(f"(Ancho: {ancho} mm)\n")
        lista_de_cadenas_de_texto_de_codigo_G.append(f"(Ancho: {ancho} mm)")
        if isinstance(angulo, list):
            for k in range(len(angulo)):
                archivo.write(f"(Angulo capa {k+1}: {angulo[k]} grados)\n")
                lista_de_cadenas_de_texto_de_codigo_G.append(f"(Angulo capa {k+1}: {angulo[k]} grados)")
        else:
            archivo.write(f"(Angulo: {angulo} grados)\n")
            lista_de_cadenas_de_texto_de_codigo_G.append(f"(Angulo: {angulo} grados)")
        if isinstance(multiples_capas, list):
            linea=7
            for j in range(len(multiples_capas)):
                archivo.write(f"(La capa {j+1} empieza en la linea: {linea})\n")
                lista_de_cadenas_de_texto_de_codigo_G.append(f"(La capa {j+1} empieza en la linea: {linea})")
                linea=linea+multiples_capas[j]+2
        else:
            archivo.write(f"(Cantidad de lineas del codigo G: {multiples_capas+7})\n")
            lista_de_cadenas_de_texto_de_codigo_G.append(f"(Cantidad de lineas del codigo G: {multiples_capas+7})")
        archivo.write(f"(N0000) G00 X 0 Y 0 A 0 \n")
        lista_de_cadenas_de_texto_de_codigo_G.append(f"(N0000) G00 X 0 Y 0 A 0")
        for i in range(num_filas):
            X=matriz_general_de_capas[i][0]
            Y=matriz_general_de_capas[i][1]
            A=matriz_general_de_capas[i][2]
            F=matriz_general_de_capas[i][3]
            num_linea=str(i+1)
            if (i+1)<9:
                N=f"(N0000{num_linea})"
            if 9<(i+1)<99:
                N=f"(N000{num_linea})"
            if 99<(i+1)<999:
                N=f"(N00{num_linea})"
            if 999<(i+1)<9999:
                N=f"(N0{num_linea})"
            if 9999<(i+1):
                N=f"(N{num_linea})"
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