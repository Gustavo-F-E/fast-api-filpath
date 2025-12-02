import uuid
import json

from clase_capa import GeneradorPatrones
from txt_G_code3 import txt_G_code3
from diccionario_txt_codigo_G import diccionario_txt_codigo_G

# Creando una instancia con parámetros personalizados
capa_1 = GeneradorPatrones(alfa=89,diametro_mandril=152.4, longitud_util=600, pines=False, coeficiente_rozamiento=0.2, ancho=20)
capa_1.ejecutar(False, False)
capa_1.seleccionar_patron()
capa_1.graficar_patron_elegido(False)
capa_1.generar_puntos_codigo_g()
capa_1.sqlite3("centrifuga", "capa_1_89")

# Creando una instancia con parámetros personalizados
capa_2 = GeneradorPatrones(alfa=89,diametro_mandril=153.2, longitud_util=600, pines=False, coeficiente_rozamiento=0.2, ancho=20)
capa_2.ejecutar(False, False)
capa_2.seleccionar_patron()
capa_2.graficar_patron_elegido(False)
capa_2.generar_puntos_codigo_g()
capa_2.sqlite3("centrifuga", "capa_2_89")

# Creando una instancia con parámetros personalizados
capa_3 = GeneradorPatrones(alfa=55,diametro_mandril=154, longitud_util=740, pines=True, coeficiente_rozamiento=0.2, ancho=17.5)
capa_3.ejecutar(False, False)
capa_3.seleccionar_patron()
capa_3.graficar_patron_elegido(False)
capa_3.generar_puntos_codigo_g()
capa_3.sqlite3("centrifuga", "capa_3_55")

# Creando una instancia con parámetros personalizados
capa_4 = GeneradorPatrones(alfa=15,diametro_mandril=154.8, longitud_util=740, pines=True, coeficiente_rozamiento=0.2, ancho=15)
capa_4.ejecutar(False, False)
capa_4.seleccionar_patron()
capa_4.graficar_patron_elegido(False)
capa_4.generar_puntos_codigo_g()
capa_4.sqlite3("centrifuga", "capa_4_15")

# Creando una instancia con parámetros personalizados
capa_5 = GeneradorPatrones(alfa=15,diametro_mandril=155.6, longitud_util=740, pines=True, coeficiente_rozamiento=0.2, ancho=15)
capa_5.ejecutar(False, False)
capa_5.seleccionar_patron()
capa_5.graficar_patron_elegido(False)
capa_5.generar_puntos_codigo_g()
capa_5.sqlite3("centrifuga", "capa_5_15")

# Creando una instancia con parámetros personalizados
capa_6 = GeneradorPatrones(alfa=55,diametro_mandril=156.4, longitud_util=740, pines=True, coeficiente_rozamiento=0.2, ancho=17.5)
capa_6.ejecutar(False, False)
capa_6.seleccionar_patron()
capa_6.graficar_patron_elegido(False)
capa_6.generar_puntos_codigo_g()
capa_6.sqlite3("centrifuga", "capa_6_55")

# Creando una instancia con parámetros personalizados
capa_7 = GeneradorPatrones(alfa=89,diametro_mandril=157.2, longitud_util=600, pines=False, coeficiente_rozamiento=0.2, ancho=20)
capa_7.ejecutar(False, False)
capa_7.seleccionar_patron()
capa_7.graficar_patron_elegido(False)
capa_7.generar_puntos_codigo_g()
capa_7.sqlite3("centrifuga", "capa_7_89")

# Creando una instancia con parámetros personalizados
capa_8 = GeneradorPatrones(alfa=89,diametro_mandril=158, longitud_util=600, pines=False, coeficiente_rozamiento=0.2, ancho=20)
capa_8.ejecutar(False, False)
capa_8.seleccionar_patron()
capa_8.graficar_patron_elegido(False)
capa_8.generar_puntos_codigo_g()
capa_8.sqlite3("centrifuga", "capa_8_89")

# Creando una instancia con parámetros personalizados
MYLAR = GeneradorPatrones(alfa=89,diametro_mandril=158.8, longitud_util=800, pines=False, coeficiente_rozamiento=0.2, ancho=20)
MYLAR.ejecutar(False, False)
MYLAR.seleccionar_patron()
MYLAR.graficar_patron_elegido(False)
MYLAR.generar_puntos_codigo_g()
MYLAR.sqlite3("centrifuga", "MYLAR")

def lista_de_capas(lista_de_capas, nombre_capa):
    diccionario_txt_codigo_G(lista_de_capas, nombre_capa)

    diccionario_codigo_G = txt_G_code3(lista_de_capas, nombre_capa)

lista_de_capas([capa_1],"capa_1_89")
lista_de_capas([capa_2],"capa_2_89")
lista_de_capas([capa_3],"capa_3_55")
lista_de_capas([capa_4],"capa_4_15")
lista_de_capas([capa_5],"capa_5_15")
lista_de_capas([capa_6],"capa_6_55")
lista_de_capas([capa_7],"capa_7_89")
lista_de_capas([capa_8],"capa_8_89")
lista_de_capas([MYLAR],"MYLAR")