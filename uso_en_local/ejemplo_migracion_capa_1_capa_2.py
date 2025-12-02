
from funcion_capa import (
    crear_diccionario_capa,
    guardar_json,
    calculos_iniciales,
    generar_patrones,
    seleccionar_patron,
    grafico_patron_elegido,
    puntos_codigo_g,
    insertar_en_sqlite3,
    txt_G_code
)

diccionario_capa_1 = crear_diccionario_capa(
    alfa=45,
    diametro_mandril=100,
    longitud_util=550,
    pines=True,
    coeficiente_rozamiento=0.2,
    ancho=5.5
)

guardar_json(diccionario_capa_1)
calculos_iniciales(diccionario_capa_1)
patrones, listas_de_patrones = generar_patrones(diccionario_capa_1)
seleccionar_patron(diccionario_capa_1, patrones, listas_de_patrones, parametro=1)
grafico_patron_elegido(diccionario_capa_1, guardar_grafico=False)
puntos_codigo_g(diccionario_capa_1)
insertar_en_sqlite3(diccionario_capa_1, usuario="pepe", nombre="capa_1")

print("\n✓ Capa 1 completada con éxito")

diccionario_capa_2 = crear_diccionario_capa(
    alfa=85,
    diametro_mandril=100,
    longitud_util=550,
    pines=True,
    coeficiente_rozamiento=0.2,
    ancho=5.5
)

guardar_json(diccionario_capa_2)
calculos_iniciales(diccionario_capa_2)
patrones, listas_de_patrones = generar_patrones(diccionario_capa_2)
seleccionar_patron(diccionario_capa_2, patrones, listas_de_patrones, parametro=1)
grafico_patron_elegido(diccionario_capa_2, guardar_grafico=False)
puntos_codigo_g(diccionario_capa_2)
insertar_en_sqlite3(diccionario_capa_2, usuario="pepe", nombre="capa_1")

print("\n✓ Capa 2 completada con éxito")

diccionario_txt_codigo_G = txt_G_code([diccionario_capa_1, diccionario_capa_2], "Capas 1 y 2")
print("codigo G generado para capas 1 y 2")
print(diccionario_txt_codigo_G)