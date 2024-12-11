def txt_G_code(diccionario_capa):

    PI = diccionario_capa["PI"]
    diametro_mandril = diccionario_capa["diametro_mandril"]
    longitud_util = diccionario_capa["longitud_util"]
    alfa = diccionario_capa["alfa"]
    ancho = diccionario_capa["ancho"]
    patron_elegido = diccionario_capa["patron_elegido_Nº"]
    puntos_codigoG = diccionario_capa["puntos_codigo_g"]
    
    alfa_gra = alfa*180/PI #Ángulo de la capa
    nombre_archivo=f"diam={diametro_mandril}_long={longitud_util}_ang={alfa_gra}_ancho={ancho}_patron={patron_elegido}.txt"
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
            X=puntos_codigoG[i][0]
            Y=puntos_codigoG[i][1]
            A=puntos_codigoG[i][2]
            F=puntos_codigoG[i][3]
            num_linea=str(i+1)
            if (i+1)<9:
                N=f"N000{num_linea}"
            if 9<(i+1)<99:
                N=f"N00{num_linea}"
            if 99<(i+1)<999:
                N=f"N0{num_linea}"
            if 999<(i+1)<9999:
                N=f"N{num_linea}"
            # Escribir línea con valores de X, Y, A y F formateados a dos decimales
            archivo.write(f"{N} G01 X {X:.2f} Y {Y:.2f} A {A:.2f} F {F:.2f}\n")