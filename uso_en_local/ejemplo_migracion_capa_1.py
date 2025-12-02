# ==============================================================================
# EJEMPLO DE MIGRACIÓN: Capa_1 usando AMBAS FORMAS
# ==============================================================================
# Este archivo muestra cómo generar la MISMA capa_1 de dos formas:
# 1. Usando la clase GeneradorPatrones (forma antigua)
# 2. Usando funciones de funcion_capa.py (forma nueva)
# ==============================================================================

print("=" * 80)
print("EJEMPLO DE MIGRACIÓN: Capa_1 - AMBAS FORMAS")
print("=" * 80)

# ==============================================================================
# FORMA 1: USANDO LA CLASE GeneradorPatrones (método original)
# ==============================================================================
print("\n" + "=" * 80)
print("FORMA 1: USANDO CLASE GeneradorPatrones")
print("=" * 80)

from clase_capa import GeneradorPatrones
from txt_G_code3 import txt_G_code3
'''
print("\n[1] Creando instancia de la clase...")
capa_1_clase = GeneradorPatrones(
    alfa=45,
    diametro_mandril=100,
    longitud_util=550,
    pines=True,
    coeficiente_rozamiento=0.2,
    ancho=5.5
)

print("[2] Ejecutando generador (calculos + patrones)...")
capa_1_clase.ejecutar(False, False)

print("[3] Seleccionando patrón #1...")
capa_1_clase.seleccionar_patron(1)

print("[4] Graficando patrón elegido...")
capa_1_clase.graficar_patron_elegido(False)

print("[5] Generando puntos de código G...")
capa_1_clase.generar_puntos_codigo_g()

print("[6] Insertando en SQLite3...")
capa_1_clase.sqlite3("pepe", "capa_1")

print("\n✓ Forma 1 completada con éxito")

'''
# ==============================================================================
# FORMA 2: USANDO FUNCIONES de funcion_capa.py (método nuevo)
# ==============================================================================
print("\n" + "=" * 80)
print("FORMA 2: USANDO FUNCIONES de funcion_capa.py")
print("=" * 80)

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

print("\n[1] Creando diccionario de parámetros...")
diccionario_capa_1 = crear_diccionario_capa(
    alfa=45,
    diametro_mandril=100,
    longitud_util=550,
    pines=True,
    coeficiente_rozamiento=0.2,
    ancho=5.5
)

print("\n[2] Guardando JSON inicial...")
guardar_json(diccionario_capa_1)

print("[3] Ejecutando cálculos iniciales...")
calculos_iniciales(diccionario_capa_1)

print("[4] Generando patrones...")
patrones, listas_de_patrones = generar_patrones(diccionario_capa_1)

print("[5] Seleccionando patrón #1...")
seleccionar_patron(diccionario_capa_1, patrones, listas_de_patrones, parametro=1)

print("[6] Graficando patrón elegido...")
grafico_patron_elegido(diccionario_capa_1, guardar_grafico=False)

print("[7] Generando puntos de código G...")
puntos_codigo_g(diccionario_capa_1)

print("[8] Insertando en SQLite3...")
insertar_en_sqlite3(diccionario_capa_1, usuario="pepe", nombre="capa_1")

print("\n✓ Forma 2 completada con éxito")


# ==============================================================================
# COMPARACIÓN DE RESULTADOS
# ==============================================================================
'''
print("\n" + "=" * 80)
print("COMPARACIÓN DE DATOS GENERADOS")
print("=" * 80)

print("\n[FORMA 1 - Clase] Parámetros calculados:")
print(f"  NP (número de puntos): {capa_1_clase.diccionario_capa.get('NP', 'N/A')}")
print(f"  DELTA: {capa_1_clase.diccionario_capa.get('DELTA', 'N/A')}")
print(f"  PASO_HELICE: {capa_1_clase.diccionario_capa.get('PASO_HELICE', 'N/A')}")
print(f"  CANTIDAD_VUELTAS_HELICE: {capa_1_clase.diccionario_capa.get('CANTIDAD_VUELTAS_HELICE', 'N/A')}")

print("\n[FORMA 2 - Funciones] Parámetros calculados:")
print(f"  NP (número de puntos): {diccionario_capa_1.get('NP', 'N/A')}")
print(f"  DELTA: {diccionario_capa_1.get('DELTA', 'N/A')}")
print(f"  PASO_HELICE: {diccionario_capa_1.get('PASO_HELICE', 'N/A')}")
print(f"  CANTIDAD_VUELTAS_HELICE: {diccionario_capa_1.get('CANTIDAD_VUELTAS_HELICE', 'N/A')}")

# Verificar si los valores coinciden
print("\n[VERIFICACIÓN]")
if capa_1_clase.diccionario_capa.get('NP') == diccionario_capa_1.get('NP'):
    print("✓ NP coinciden")
else:
    print("✗ NP NO coinciden")

if capa_1_clase.diccionario_capa.get('DELTA') == diccionario_capa_1.get('DELTA'):
    print("✓ DELTA coincide")
else:
    print("✗ DELTA NO coincide")

if capa_1_clase.diccionario_capa.get('PASO_HELICE') == diccionario_capa_1.get('PASO_HELICE'):
    print("✓ PASO_HELICE coincide")
else:
    print("✗ PASO_HELICE NO coincide")
'''
# ==============================================================================
# GUÍA DE MIGRACIÓN RÁPIDA
# ==============================================================================
print("\n" + "=" * 80)
print("GUÍA DE MIGRACIÓN RÁPIDA")
print("=" * 80)

print("""
Para migrar tu código de la CLASE a FUNCIONES:

1. CAMBIAR IMPORTACIONES:
   De:  from clase_capa import GeneradorPatrones
   A:   from funcion_capa import (crear_diccionario_capa, guardar_json, ...)

2. CAMBIAR CREACIÓN:
   De:  capa = GeneradorPatrones(alfa=45, ...)
   A:   capa = crear_diccionario_capa(alfa=45, ...)
        guardar_json(capa)

3. CAMBIAR LLAMADAS A MÉTODOS:
   De:  capa.ejecutar(False, False)
   A:   calculos_iniciales_func(capa)
        patrones, listas = generar_patrones_func(capa)

4. CAMBIAR SELECCIÓN DE PATRÓN:
   De:  capa.seleccionar_patron(1)
   A:   seleccionar_patron_func(capa, patrones, listas, parametro=1)

5. CAMBIAR OTROS MÉTODOS:
   De:  capa.graficar_patron_elegido(False)
   A:   graficar_patron_elegido_func(capa, guardar_grafico=False)

   De:  capa.generar_puntos_codigo_g()
   A:   puntos_codigo_g_func(capa)

   De:  capa.sqlite3("usuario", "nombre")
   A:   insertar_en_sqlite3_func(capa, usuario="usuario", nombre="nombre")

6. ACCESO A DATOS:
   De:  capa.diccionario_capa["NP"]
   A:   capa["NP"]
""")

print("\n" + "=" * 80)
print("FIN DEL EJEMPLO")
print("=" * 80)

'''
diccionario_txt_codigo_G_A = txt_G_code3([capa_1_clase], "Capas 1")
print("codigo G generado para capas 1 primer metodo")
print(diccionario_txt_codigo_G_A )
'''
diccionario_txt_codigo_G_B = txt_G_code([diccionario_capa_1], "Capas 1")
print("codigo G generado para capas 1 segundo metodo")
print(diccionario_txt_codigo_G_B )