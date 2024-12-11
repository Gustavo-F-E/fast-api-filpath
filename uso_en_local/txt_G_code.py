def txt_G_code(lista_de_capas):
    numero_de_capas = len(lista_de_capas)
    diametro_mandril = lista_de_capas[0].diccionario_capa["diametro_mandril"]
    longitud_util = lista_de_capas[0].diccionario_capa["longitud_util"]
    ancho = lista_de_capas[0].diccionario_capa["ancho"]
    nombre_archivo = f"diam={diametro_mandril}_long={longitud_util}_ancho={ancho}.txt"
    
    try:
        desfasajes = desfasajes_entre_capas(lista_de_capas)
    except IndexError:
        raise IndexError("Error al calcular 'desfasajes': el tamaño de 'lista_de_capas' o los datos en 'diccionario_capa' están incompletos.")
    
    XX = 0  # Avance del eje X en la última pasada de cada capa

    try:
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(f"(Código G generado por Gustavo Francisco Eichhorn)\n\n")
            archivo.write(f"(Diámetro del mandril: {diametro_mandril} mm)\n\n")
            archivo.write(f"(Longitud del mandril: {longitud_util} mm)\n\n")
            archivo.write(f"(Ancho: {ancho} mm)\n\n")

            for j in range(numero_de_capas):
                puntos_codigoG = lista_de_capas[j].diccionario_capa.get("puntos_codigo_g")
                
                '''
                puntos_codigo_g=lista_de_capas[0].diccionario_capa["puntos_codigo_g"]
                maximo=puntos_codigo_g[2][1]
                puntos_codigo_g[:,1] += maximo #Le añado el maximo para correr el cero
                '''
                
                if puntos_codigoG is None:
                    raise KeyError(f"Error: 'puntos_codigo_g' no encontrado en 'diccionario_capa' de la capa {j}.")
                
                num_filas = puntos_codigoG.shape[0]
                
                if j == 0:
                    archivo.write("N0000 G00 X 0 Y 0 A 0 \n")
                    contador = 1
                
                for i in range(num_filas):
                    try:
                        X = puntos_codigoG[i][0] + XX
                        Y = puntos_codigoG[i][1] + desfasajes[i]
                        A = puntos_codigoG[i][2]
                        F = puntos_codigoG[i][3]
                    except IndexError:
                        raise IndexError(f"Error: 'puntos_codigo_g' en la capa {j} no tiene suficientes valores en la fila {i}.")
                    
                    num_linea = str(contador)
                    if (i + 1) < 9:
                        N = f"N0000{num_linea}"
                    elif 9 < (i + 1) < 99:
                        N = f"N000{num_linea}"
                    elif 99 < (i + 1) < 999:
                        N = f"N00{num_linea}"
                    elif 999 < (i + 1) < 9999:
                        N = f"N0{num_linea}"
                    else:
                        N = f"N{num_linea}"
                    
                    archivo.write(f"{N} G01 X {X:.2f} Y {Y:.2f} A {A:.2f} F {F:.2f}\n")

                    # Código adicional en caso de última fila
                    if i == num_filas - 1:
                        incremento_X = puntos_codigoG[i][0] - puntos_codigoG[i - 1][0]
                        if i + 1 < len(desfasajes):
                            X2 = X + incremento_X
                            Y2 = Y - (desfasajes[i + 1] - desfasajes[i]) if desfasajes[i] <= desfasajes[i + 1] else Y + (desfasajes[i + 1] - desfasajes[i])
                            archivo.write(f"{N} G01 X {X2:.2f} Y {Y2:.2f} A {A:.2f} F {F:.2f}\n")
                            XX += X2
                        else:
                            raise IndexError("Error: índice fuera de rango en 'desfasajes' en la capa {j}, fila {i}. Revisa la longitud de 'desfasajes'.")
                    
                    contador += 1

    except Exception as e:
        print(f"Ocurrió un error al escribir el código G: {e}")

def desfasajes_entre_capas(lista_de_capas):
    desfasajes=[]
    maximos=[]
    numero_de_capas=len(lista_de_capas)
    
    for i in range(numero_de_capas):
        maximo=lista_de_capas[i].diccionario_capa["L_retorno"]+lista_de_capas[i].diccionario_capa["longitud_util"]/2
        maximos.append(maximo)
    
    for j in range(numero_de_capas):
        desfasaje=maximos[j]-max(maximos)
        desfasajes.append(desfasaje+maximos[j]) #me calcula el desfasaje desde el cero
    
    return desfasajes