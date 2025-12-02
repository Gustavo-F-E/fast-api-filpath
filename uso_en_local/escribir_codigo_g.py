import json

def escribir_codigo_g(matriz_general_de_capas, lista_de_capas, i, angulo, multiples_capas, diccionario_codigo_G, nombre_del_estudio):
    diametro_mandril = lista_de_capas[0].diccionario_capa["diametro_mandril"]
    longitud_util = lista_de_capas[0].diccionario_capa["longitud_util"]
    ancho = lista_de_capas[0].diccionario_capa["ancho"]
    
    lista_de_cadenas_de_texto_de_codigo_G=[]
    #print("type(diccionario_codigo_G) 1 escribir_codigo_g")
    #print(type(diccionario_codigo_G))
    # Genera un UUID y conviértelo a una cadena de texto
    ii=i
    if i==-1:
        texto=f"Total_{nombre_del_estudio}"
        #uuid_aleatorio = str(uuid.uuid4())
        #uuid_6=uuid_aleatorio[:6] # Puedes recortar a la longitud que desees si necesitas menos de 36 caracteres
        uuid_6 = lista_de_capas[0].diccionario_capa["uuid_6"]
    elif i==-2:
        texto=f"Capa_Unica_{nombre_del_estudio}"
        uuid_6 = lista_de_capas[0].diccionario_capa["uuid_6"]
    else:
        texto=f"Capa_{str(i+1)}_{nombre_del_estudio}"
        uuid_6 = lista_de_capas[0].diccionario_capa["uuid_6"]
    
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
