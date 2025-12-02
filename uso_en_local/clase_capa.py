import math
import json
import uuid
import os
import sqlite3
from calculos_iniciales import calculos_iniciales
from vinogradov import vinodradov, obteniendo_orden_del_patron
from grafico_de_patrones import orden_de_listas_areas, graficar_multiples_areas
from grafico_patron_elegido import grafico_patron_elegido
from grafico_patron_elegido_2 import grafico_patron_elegido_2
from puntos_codigo_g import puntos_codigo_g
from txt_G_code2 import txt_G_code
from txt_G_code3 import txt_G_code3

class GeneradorPatrones:
    def __init__(self, diametro_mandril=100, longitud_util=360, alfa=45, ancho=6.5, exceso_de_resina=False, corregir_angulo=False, pines=False, coeficiente_rozamiento=0.2, espesor=0.2, velocidad_de_alimentacion=9000):
        
        uuid_aleatorio = str(uuid.uuid4())
        uuid_6=uuid_aleatorio[:6] # Puedes recortar a la longitud que desees si necesitas menos de 36 caracteres
        self.filename=f"diam_{diametro_mandril}_long={longitud_util}_ancho={ancho}_alfa={alfa}_{uuid_6}.json"
        self.filename2=f"diam_{diametro_mandril}_long={longitud_util}_ancho={ancho}_alfa={alfa}_{uuid_6}"
        
        self.diccionario_capa = {
            "filename": self.filename,
            "filename2": self.filename2,
            "uuid_6": uuid_6,
            "PI": math.pi,
            "diametro_mandril": diametro_mandril,
            "longitud_util": longitud_util,
            "alfa": alfa,
            "alfa_original": alfa,
            "ancho": ancho,
            "exceso_de_resina": exceso_de_resina,
            "corregir_angulo": corregir_angulo,
            "pines": pines,
            "coeficiente_rozamiento": coeficiente_rozamiento,
            "espesor": espesor,
            "velocidad_de_alimentacion": velocidad_de_alimentacion
        }
        # Crear el archivo JSON automáticamente
        self.JSON()
        

    def JSON(self):
        try:
            with open(self.filename, 'w') as json_file:
                json.dump(self.diccionario_capa, json_file, indent=4)
            print(f"Archivo JSON '{self.filename}' creado exitosamente.")
        except Exception as e:
            print(f"Error al crear el archivo JSON: {e}")
    
    def obtener_parametros_iniciales(self):
        calculos_iniciales(self.diccionario_capa)

    def generar_patrones(self):
        self.patrones = vinodradov(self.diccionario_capa)
        self.listas_de_patrones = [
            obteniendo_orden_del_patron(self.diccionario_capa["NP"], patron[3])
            for patron in self.patrones
        ]
        self.diccionario_capa["listas_de_patrones"] = self.listas_de_patrones
        self.diccionario_capa["patrones"] = self.patrones
        
        # Obtener el nombre del archivo
        filename = self.diccionario_capa["filename"]
        
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
        datos_existentes["lista_de_patrones"] = self.listas_de_patrones
        datos_existentes["patrones"] = self.patrones

        # Escribir el diccionario actualizado en el archivo JSON
        try:
            with open(filename, 'w') as json_file:
                json.dump(datos_existentes, json_file, indent=4)
            print(f"Archivo JSON '{filename}' actualizado exitosamente.")
        except Exception as e:
            print(f"Error al escribir el archivo JSON: {e}")

    def graficar_patrones(self, guardar_grafico, graficar_solo_esquemas):
        for index, lista in enumerate(self.listas_de_patrones):
            lista = orden_de_listas_areas(self.diccionario_capa["NP"], lista)
            paso = self.patrones[index][3]
            ptr = self.patrones[index][1]
            Dcco = self.patrones[index][4]
            orden = self.listas_de_patrones[index]
            #graficar_multiples_areas(lista, self.diccionario_capa["NP"], paso, index, orden, ptr, Dcco, self.diccionario_capa, guardar_grafico, graficar_solo_esquemas)

    def seleccionar_patron(self, parametro=None):
        if parametro is None:
            # Si no se proporciona un parámetro, calcula el patrón elegido por defecto
            patron_elegido = 1 + min(enumerate(self.patrones), key=lambda x: abs(x[1][4]))[0]
        else:
            # Si se proporciona un parámetro, úsalo como el patrón elegido
            patron_elegido = parametro

        # Obtiene el orden de patrones basado en el patrón elegido
        orden_de_patrones = self.listas_de_patrones[patron_elegido - 1]

        # Actualiza el diccionario con la información del patrón elegido
        self.diccionario_capa.update({
            "patron_elegido_Nº": patron_elegido,
            "orden_del_patron_elegido": orden_de_patrones,
            "PTR": self.patrones[patron_elegido - 1][1],
            "Paso": self.patrones[patron_elegido - 1][3],
            "Dcco": self.patrones[patron_elegido - 1][4]
        })
        
        # Crear la lista de cálculos iniciales
        patron_elegido = [
            {"patron_elegido_Numero": patron_elegido},
            {"orden_del_patron_elegido": orden_de_patrones},
            {"PTR": self.patrones[patron_elegido - 1][1]},
            {"Paso": self.patrones[patron_elegido - 1][3]},
            {"Dcco": self.patrones[patron_elegido - 1][4]}
        ]
        
        # Obtener el nombre del archivo
        filename = self.diccionario_capa["filename"]
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
        datos_existentes["patron_elegido"] = patron_elegido

        # Escribir el diccionario actualizado en el archivo JSON
        try:
            with open(filename, 'w') as json_file:
                json.dump(datos_existentes, json_file, indent=4)
            print(f"Archivo JSON '{filename}' actualizado exitosamente.")
        except Exception as e:
            print(f"Error al escribir el archivo JSON: {e}")

    def graficar_patron_elegido(self, guardar_grafico):
        grafico_patron_elegido(self.diccionario_capa, guardar_grafico)
    
    def graficar_patron_elegido_2(self, guardar_grafico):
        grafico_patron_elegido_2(self.diccionario_capa, guardar_grafico)

    def generar_puntos_codigo_g(self):
        puntos_codigo_g(self.diccionario_capa)

    def generar_txt_G_code(self):
        txt_G_code(self.diccionario_capa)
    
    def generar_txt_G_code3(self):
        txt_G_code3(self.diccionario_capa)

    def ejecutar(self, guardar_grafico, graficar_solo_esquemas):
        self.obtener_parametros_iniciales()
        self.generar_patrones()
        self.graficar_patrones(guardar_grafico, graficar_solo_esquemas)        
    def sqlite3(self, usuario, nombre):
        diccionario_capa=self.diccionario_capa
        filename2=diccionario_capa["filename2"]
        diametro_mandril=diccionario_capa["diametro_mandril"]
        longitud_util=diccionario_capa["longitud_util"]
        espesor=diccionario_capa["espesor"]
        coeficiente_rozamiento=diccionario_capa["coeficiente_rozamiento"]
        pines=diccionario_capa["pines"]
        alfa=diccionario_capa["alfa"]
        alfa_original=diccionario_capa["alfa_original"]
        ancho=diccionario_capa["ancho"]
        exceso_de_resina=diccionario_capa["exceso_de_resina"]
        corregir_angulo=diccionario_capa["corregir_angulo"]
        velocidad_de_alimentacion=diccionario_capa["velocidad_de_alimentacion"]
        alfa_corregido=diccionario_capa["calculos_iniciales"][1]["alfa_corregido"]
        ancho_eff=diccionario_capa["calculos_iniciales"][2]["ancho_eff"]
        NP=diccionario_capa["calculos_iniciales"][4]["NP"]
        patron_elegido=diccionario_capa["patron_elegido_Nº"]
        orden_del_patron_elegido=diccionario_capa["orden_del_patron_elegido"]
        PTR=diccionario_capa["PTR"]
        Paso=diccionario_capa["Paso"]
        Dcco=diccionario_capa["Dcco"]
        puntos_codigo_g_centrados=diccionario_capa["puntos_codigo_g"]
        # Conectar a la base de datos (la base de datos se creará si no existe) 
        conn = sqlite3.connect('capas.db') 
        # Crear un cursor 
        cursor = conn.cursor()
        cursor.execute(''' INSERT INTO capas (
        usuario,
        nombre,
        filename2,
        diametro_mandril,
        longitud_util,
        espesor,
        coeficiente_rozamiento,
        pines,
        alfa_original,
        ancho,
        exceso_de_resina,
        corregir_angulo,
        velocidad_de_alimentacion,
        alfa_corregido,
        ancho_eff,
        NP,
        patron_elegido,
        orden_del_patron_elegido,
        PTR,
        Paso,
        Dcco,
        puntos_codigo_g
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', (
        usuario,
        nombre,
        filename2,
        diametro_mandril,
        longitud_util,
        espesor,
        coeficiente_rozamiento,
        pines,
        alfa_original,
        ancho,
        exceso_de_resina,
        corregir_angulo,
        velocidad_de_alimentacion,
        alfa_corregido,
        ancho_eff,
        NP,
        patron_elegido,
        str(orden_del_patron_elegido),
        PTR,
        Paso,
        Dcco,
        str(puntos_codigo_g_centrados)
        ))
        conn.commit()
        conn.close()
        
    def guardar_diccionario_capa_como_json(self, ruta_relativa, nombre_archivo): # Crear la ruta completa 
        ruta_completa = os.path.join(ruta_relativa, nombre_archivo) 
        # Crear el directorio si no existe 
        os.makedirs(ruta_relativa, exist_ok=True) 
        # Guardar el diccionario en el archivo JSON 
        with open(ruta_completa, 'w') as f: 
            json.dump(self.diccionario_capa, f) 
        return ruta_completa

        def to_dict(self):
            return {
                'usuario': self.usuario,
                'nombre': self.nombre,
                'filename2': self.diccionario_capa['filename2'],
                'diametro_mandril': self.diccionario_capa['diametro_mandril'],
                'longitud_util': self.diccionario_capa['longitud_util'],
                'espesor': self.diccionario_capa['espesor'],
                'coeficiente_rozamiento': self.diccionario_capa['coeficiente_rozamiento'],
                'pines': self.diccionario_capa['pines'],
                'alfa_original': self.diccionario_capa['alfa_original'],
                'ancho': self.diccionario_capa['ancho'],
                'exceso_de_resina': self.diccionario_capa['exceso_de_resina'],
                'corregir_angulo': self.diccionario_capa['corregir_angulo'],
                'velocidad_de_alimentacion': self.diccionario_capa['velocidad_de_alimentacion'],
                'alfa_corregido': self.diccionario_capa.get('alfa_corregido', None),
                'ancho_eff': self.diccionario_capa.get('ancho_eff', None),
                'NP': self.diccionario_capa.get('NP', None),
                'patron_elegido': self.diccionario_capa.get('patron_elegido_Nº', None),
                'orden_del_patron_elegido': str(self.diccionario_capa.get('orden_del_patron_elegido', None)),
                'PTR': self.diccionario_capa.get('PTR', None),
                'Paso': self.diccionario_capa.get('Paso', None),
                'Dcco': self.diccionario_capa.get('Dcco', None),
                'puntos_codigo_g': str(self.diccionario_capa.get('puntos_codigo_g', None))
            }