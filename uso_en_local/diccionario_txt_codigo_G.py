import uuid
import json
from txt_G_code3 import txt_G_code3

def diccionario_txt_codigo_G(lista_de_capas):
    diccionario_codigo_G = txt_G_code3(lista_de_capas)
    print("Main")
    if len(lista_de_capas)==1:
      print("")
      lista=diccionario_codigo_G["Capa_Unica"]
      for i in range(len(lista)):
        print(lista[i])
    if len(lista_de_capas)!=1:
        for i in range(len(lista_de_capas)):
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
      
    diametro_mandril=lista_de_capas[0].diccionario_capa["diametro_mandril"]
    longitud_util=lista_de_capas[0].diccionario_capa["longitud_util"]
    ancho=lista_de_capas[0].diccionario_capa["ancho"]
    uuid_aleatorio = str(uuid.uuid4())
    uuid_6=uuid_aleatorio[:6] # Puedes recortar a la longitud que desees si necesitas menos de 36 caracteres
    filename=f"diam_{diametro_mandril}_long={longitud_util}_ancho={ancho}_{uuid_6}_G_code.json"
    try:
        with open(filename, 'w') as json_file:
            json.dump(diccionario_codigo_G, json_file, indent=4)
        print(f"Archivo JSON '{filename}' creado exitosamente.")
    except Exception as e:
        print(f"Error al crear el archivo JSON: {e}")