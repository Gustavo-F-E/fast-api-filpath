from vinogradov import vinodradov
from vinogradov import obteniendo_orden_del_patron
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
import json
import sqlite3


def graficar_patrones(diccionario_capa, guardar_grafico, graficar_solo_esquemas, i, filename):
    for index, lista in enumerate(diccionario_capa["listas_de_patrones"]):
        lista = orden_de_listas_areas(diccionario_capa["NP"], lista)
        paso = diccionario_capa["patrones"][index][3]
        ptr = diccionario_capa["patrones"][index][1]
        Dcco = diccionario_capa["patrones"][index][4]
        orden = diccionario_capa["listas_de_patrones"][index]
        graficar_multiples_areas(lista, diccionario_capa["NP"], paso, index, orden, ptr, Dcco, diccionario_capa, guardar_grafico, graficar_solo_esquemas, i, filename)

def dibujar_area(puntos, ax, color, N):
    # Separar las coordenadas X e Y de los puntos
    x, y = zip(*puntos)
    
    # Dibujar el polígono cerrando la figura al unir el primer y último punto
    ax.fill(x, y, color, edgecolor='black')  # Relleno con el color especificado y bordes negros

    # Configurar límites del gráfico si es necesario (opcional)
    ax.set_xlim(0, N)
    ax.set_ylim(0, N)

# Llamar a la función para generar las áreas
def areas_patron(N):
    x0 = []
    xN = []
    y0 = []
    yN = []
    for i in range(0, N + 1):
        x0.append((0, i))
        xN.append((N, i))
        y0.append((i, 0))
        yN.append((i, N))
    
    areas_x = []
    areas_y = []
    for k in range(0, N):
        kx=k
        ky=N-1-k
        areas_x.append([y0[kx], yN[kx], yN[kx + 1], y0[kx + 1]])  # Llenamos áreas x
        areas_y.append([x0[ky], x0[ky + 1], xN[ky + 1], xN[ky]])  # Llenamos áreas y
    
    return areas_x, areas_y

def graficar_multiples_areas(lista_de_areas, N, paso, index2, orden, ptr, Dcco, diccionario_capa, guardar_grafico, graficar_solo_esquemas, indice, filename):
    diametro_mandril = 1
    ancho = 1
    uuid_6 = 1
    longitud_util = 1
    alfa = 1
    alfa_original = 1
    NP = diccionario_capa["NP"]
    listas_de_patrones = diccionario_capa["listas_de_patrones"]

    lineas_orden = [orden[i:i + 20] for i in range(0, len(orden), 20)]

    
    # Mostrar y/o guardar el gráfico
    if graficar_solo_esquemas==True:
        nombre_archivo=f"imagenes/patrones/NP={NP}_esquema_patron_No_{index2+1}_.png"
        nombre_archivo_miniatura=f"imagenes/patrones/NP={NP}_esquema_patron_No_{index2+1}__mini.png"
    else: 
        nombre_archivo=f"imagenes/diam_{diametro_mandril}_long={longitud_util}_ancho={ancho}_alfa={alfa_original}_{uuid_6}_NP={NP}_esquema_patron_Nº_{index2+1}_.png"
    
    if guardar_grafico:
        pass

    if guardar_grafico:
        pass
    
    
    #print(orden)

    with open(filename, 'r') as json_file:
        datos_existentes = json.load(json_file) #Cargamos el JSON como un diccionario
    key=f"NP_{NP}"
    value=f"listado_patron_N_{index2+1}"
    nombre_archivo_png=f"NP={NP}_esquema_patron_No_{index2+1}_.png"

    if index2==0:
        datos_existentes[key].update({"Dcco_minimo":abs(Dcco)})
        datos_existentes[key].update({"Patron_Dcco_minimo":(index2+1)})
        cursor.execute('''
            UPDATE NP
            SET Dcco_minimo = ?, Patron_Dcco_minimo = ?
            WHERE NP = ?
            ''', (abs(Dcco), (index2+1), NP))
        # Guardar (commit) los cambios
        conexion.commit()
    else:
        if abs(Dcco)<datos_existentes[key]["Dcco_minimo"]:
            datos_existentes[key].update({"Dcco_minimo":abs(Dcco)})
            datos_existentes[key].update({"Patron_Dcco_minimo":(index2+1)})
            cursor.execute('''
                UPDATE NP
                SET Dcco_minimo = ?, Patron_Dcco_minimo = ?
                WHERE NP = ?
                ''', (abs(Dcco), (index2+1), NP))
                # Guardar (commit) los cambios
            conexion.commit()
        else: pass
    
    datos_existentes[key].update({
      value:{
        "NP": NP,
        "Paso": paso,
        "Ptr": ptr,
        "Dcco": Dcco,
        "Orden_del_patron": orden,
        "nombre_archivo": nombre_archivo_png,
        }
      })
    
    lista_orden=str(orden)
    
    cursor.execute('''
        INSERT INTO listado_de_patrones (NP, patron_numero, Paso, Ptr, Dcco, Orden_del_patron, nombre_archivo)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (NP, index2+1, paso, ptr, Dcco, lista_orden, nombre_archivo_png))
        # Guardar (commit) los cambios
    conexion.commit()
    
    #print('datos_existentes[key]["Dcco_minimo"]')
    #print(datos_existentes[key]["Dcco_minimo"])

    with open(filename, 'w') as json_file:
        json.dump(datos_existentes, json_file, ensure_ascii=False, indent=4)
    #print(f"Archivo JSON '{filename}' actualizado exitosamente.")


def orden_de_listas_areas(NP, ORDEN):
    areas_x, areas_y = areas_patron(NP)
    lista_areas = []
    
    for i in range(len(ORDEN)):  # Ajustar índice
        lista_areas.append(areas_y[ORDEN[i] - 1])
        lista_areas.append(areas_x[ORDEN[i] - 1])
    #print(lista_areas)
    return lista_areas

######################################################
######################################################
#Programa principal
diccionario_capa = {}
inicio=1
fin=100
filename="imagenes/patrones/patrones4.json"

# Conectar a la base de datos (o crearla si no existe)
conexion = sqlite3.connect('./imagenes/patrones/data.db')

# Crear un cursor para ejecutar consultas
cursor = conexion.cursor()

try:
    with open(filename, 'w') as json_file:
        datos_existentes = {}
        for j in range(inicio,fin+1):
            key=f"NP_{j}"
            datos_existentes[key]={
                "NP" : j
            }
        json.dump(datos_existentes, json_file, indent=4)
    #print(f"Archivo JSON '{filename}' actualizado exitosamente.")
except Exception as e:
    pass
    #print(f"Error al escribir el archivo JSON: {e}")


for i in range(inicio,fin+1):
    diccionario_capa["NP"] = i
    patrones = vinodradov(diccionario_capa)
    listas_de_patrones = [
        obteniendo_orden_del_patron(diccionario_capa["NP"], patron[3])
        for patron in patrones
    ]
    diccionario_capa["listas_de_patrones"] = listas_de_patrones
    diccionario_capa["patrones"] = patrones
    #print('len("listas_de_patrones")')
    #print(len(listas_de_patrones))
    

    with open(filename, 'r') as json_file:
        datos_existentes = json.load(json_file) #Cargamos el JSON como un diccionario
    key=f"NP_{i}"
    value="cantidad_de_patrones"
    datos_existentes[key].update({
      value:len(listas_de_patrones)
      })
    with open(filename, 'w') as json_file:
        json.dump(datos_existentes, json_file, indent=4)
    #print(f"Archivo JSON '{filename}' actualizado exitosamente.")
    
    cursor.execute('''
    INSERT INTO NP (NP, cantidad_de_patrones)
    VALUES (?, ?)
    ''', (i, len(listas_de_patrones)))
    # Guardar (commit) los cambios
    conexion.commit()
    
    #graficar_patrones(diccionario_capa, True, True, i)
    graficar_patrones(diccionario_capa, False, False, i, filename)
    print(i)

# Cerrar la conexión
conexion.close()