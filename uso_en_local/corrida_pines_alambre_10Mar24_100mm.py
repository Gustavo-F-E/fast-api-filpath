import uuid
import json
from clase_capa import GeneradorPatrones
from txt_G_code3 import txt_G_code3
from diccionario_txt_codigo_G import diccionario_txt_codigo_G

# Parametros por defecto: diametro_mandril=100, longitud_util=360, alfa=45, ancho=6.5, exceso_de_resina=False, corregir_angulo=False, pines=False, coeficiente_rozamiento=0.2, espesor=0.2

# Uso de la clase
capa_1 = GeneradorPatrones(alfa=45,diametro_mandril=100, longitud_util=550, pines=True, coeficiente_rozamiento=0.2, ancho=5.5)
capa_1.ejecutar(False, False)
capa_1.seleccionar_patron(1)
capa_1.graficar_patron_elegido(False)
capa_1.generar_puntos_codigo_g()
capa_1.sqlite3("pepe", "capa_1")

# Creando una instancia con parámetros personalizados
#capa_2 = GeneradorPatrones(alfa=45, diametro_mandril=100, longitud_util=550, exceso_de_resina=False, pines=True, coeficiente_rozamiento=0.2, ancho=5.5)

# Puedes ejecutar el generador o llamar a otros métodos
"""
capa_2.ejecutar(False, False)
capa_2.seleccionar_patron()
capa_2.graficar_patron_elegido(False)
capa_2.generar_puntos_codigo_g()
capa_2.sqlite3("pepe", "capa_2")
"""

# Creando una instancia con parámetros personalizados
#capa_3 = GeneradorPatrones(alfa=15, diametro_mandril=100, longitud_util=550, exceso_de_resina=False, pines=True, coeficiente_rozamiento=0.2, ancho=5.5)

# Puedes ejecutar el generador o llamar a otros métodos
#capa_3.ejecutar(False, False)
#capa_3.seleccionar_patron()
#capa_3.graficar_patron_elegido(False)
#capa_3.generar_puntos_codigo_g()
#capa_3.sqlite3("juan", "capa_3")

# Creando una instancia con parámetros personalizados
#capa_4 = GeneradorPatrones(alfa=89, diametro_mandril=100, longitud_util=550, exceso_de_resina=False, pines=True, coeficiente_rozamiento=0.2, ancho=5.5)

# Puedes ejecutar el generador o llamar a otros métodos

#capa_4.ejecutar(False, False)
#capa_4.seleccionar_patron()
#capa_4.graficar_patron_elegido(False)
#capa_4.generar_puntos_codigo_g()
#capa_4.sqlite3("juan", "capa_4")



# Creando una instancia con parámetros personalizados
#capa_MYLAR = GeneradorPatrones(alfa=89, diametro_mandril=100, longitud_util=550, exceso_de_resina=False, pines=True, coeficiente_rozamiento=0.2, ancho=12)

# Puedes ejecutar el generador o llamar a otros métodos
"""
capa_MYLAR.ejecutar(False, False)
capa_MYLAR.seleccionar_patron()
capa_MYLAR.graficar_patron_elegido(False)
capa_MYLAR.generar_puntos_codigo_g()
capa_MYLAR.sqlite3("juan", "capa_MYLAR")
"""

# Creando una instancia con parámetros personalizados
#capa_TAPON = GeneradorPatrones(alfa=45, diametro_mandril=100, longitud_util=200, exceso_de_resina=False, pines=True, coeficiente_rozamiento=0.2, ancho=5.5)

# Puedes ejecutar el generador o llamar a otros métodos
"""
capa_TAPON.ejecutar(False, False)
capa_TAPON.seleccionar_patron()
capa_TAPON.graficar_patron_elegido(False)
capa_TAPON.generar_puntos_codigo_g()
capa_TAPON.sqlite3("juan", "capa_TAPON")
"""

#Ùlista_de_capas1=[capa_1]
#lista_de_capas5=[capa_2]
#lista_de_capas3=[capa_1, capa_2]
#lista_de_capas4=[capa_2, capa_1]
#lista_de_capas5=[capa_1, capa_2, capa_3, capa_4]
lista_de_capas5=[capa_1]
#lista_de_capas5=[capa_1]
nombre_capa = "corrida_prueba_mandril_pines_alambre"
#lista_de_capas5=[capa_MYLAR]
#nombre_capa = "MYLAR"
#lista_de_capas5=[capa_TAPON]
#nombre_capa = "TAPON"

diccionario_txt_codigo_G(lista_de_capas5, nombre_capa)

diccionario_codigo_G = txt_G_code3(lista_de_capas5, nombre_capa)
"""
print("Main")
if len(lista_de_capas5)==1:
  print("")
  lista=diccionario_codigo_G["Capa_Unica"]
  for i in range(len(lista)):
    print(lista[i])
if len(lista_de_capas5)!=1:
    for i in range(len(lista_de_capas5)):
        lista=diccionario_codigo_G[f"Capa_{str(i+1)}"]
        print("")
        print(f"Capa_{str(i+1)}")
        for j in range(len(lista)):
            print(lista[j])

lista=diccionario_codigo_G["Total"]
print("")
print("Total")
for i in range(len(lista)):
  print(lista[i])
  
diametro_mandril=lista_de_capas5[0].diccionario_capa["diametro_mandril"]
longitud_util=lista_de_capas5[0].diccionario_capa["longitud_util"]
ancho=lista_de_capas5[0].diccionario_capa["ancho"]
alfa=lista_de_capas5[0].diccionario_capa["alfa"]
uuid_aleatorio = str(uuid.uuid4())
uuid_6=uuid_aleatorio[:6] # Puedes recortar a la longitud que desees si necesitas menos de 36 caracteres
filename=f"diam_{diametro_mandril}_long={longitud_util}_ancho={ancho}_alfa={alfa}_{uuid_6}.json"
try:
    with open(filename, 'w') as json_file:
        json.dump(diccionario_codigo_G, json_file, indent=4)
    print(f"Archivo JSON '{filename}' creado exitosamente.")
except Exception as e:
    print(f"Error al crear el archivo JSON: {e}")
"""

'''
# Uso de la clase
'''
"""
capa_1 = GeneradorPatrones(alfa=5, diametro_mandril=100, longitud_util=450, pines=True, coeficiente_rozamiento=0.1, ancho=5)
capa_1.ejecutar(False, False)
capa_1.seleccionar_patron(5)
capa_1.graficar_patron_elegido(False)
#capa_1.graficar_patron_elegido_2(False)
capa_1.generar_puntos_codigo_g()
lista_de_capas1=[capa_1]

diccionario_codigo_G = txt_G_code3(lista_de_capas1)
print("Main")
if len(lista_de_capas1)==1:
  lista=diccionario_codigo_G["Capa_Unica"]
  print("")
  for i in range(len(lista)):
    print(lista[i])
if len(lista_de_capas1)!=1:
    for i in range(len(lista_de_capas1)):
        lista=diccionario_codigo_G[f"Capa_{str(i+1)}"]
        print("")
        print(f"Capa_{str(i+1)}")
        for j in range(len(lista)):
            print(lista[j])

lista=diccionario_codigo_G["Total"]
print("")
print("Total")
for i in range(len(lista)):
  print(lista[i])

"""