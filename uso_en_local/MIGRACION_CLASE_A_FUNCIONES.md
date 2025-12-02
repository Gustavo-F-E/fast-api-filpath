# Migración de GeneradorPatrones (Clase) a funcion_capa.py (Funciones)

## Resumen de Cambios

La clase `GeneradorPatrones` de `clase_capa.py` ha sido convertida a un conjunto de funciones independientes en `funcion_capa.py`.

---

## Equivalencia de Código

### ANTES (Usando la Clase)
```python
from clase_capa import GeneradorPatrones

# Crear instancia de la clase
capa_1 = GeneradorPatrones(
    alfa=45,
    diametro_mandril=100, 
    longitud_util=550, 
    pines=True, 
    coeficiente_rozamiento=0.2, 
    ancho=5.5
)

# Llamar a los métodos
capa_1.ejecutar(False, False)              # Ejecuta calculos_iniciales + generar_patrones
capa_1.seleccionar_patron(1)                # Selecciona patrón específico
capa_1.graficar_patron_elegido(False)       # Grafica el patrón elegido
capa_1.generar_puntos_codigo_g()            # Genera puntos de código G
capa_1.sqlite3("pepe", "capa_1")            # Inserta en base de datos
```

### AHORA (Usando Funciones)
```python
from funcion_capa import (
    crear_diccionario_capa, 
    guardar_json,
    calculos_iniciales, 
    generar_patrones, 
    seleccionar_patron, 
    grafico_patron_elegido, 
    puntos_codigo_g, 
    insertar_en_sqlite3
)

# Crear diccionario de parámetros (en lugar de crear instancia)
capa_1 = crear_diccionario_capa(
    alfa=45,
    diametro_mandril=100, 
    longitud_util=550, 
    pines=True, 
    coeficiente_rozamiento=0.2, 
    ancho=5.5
)

# Guardar JSON inicial
guardar_json(capa_1)

# Llamar a funciones independientes
calculos_iniciales(capa_1)
patrones, listas_de_patrones = generar_patrones(capa_1)

# Seleccionar patrón (pasando patrones y listas_de_patrones)
seleccionar_patron(capa_1, patrones, listas_de_patrones, parametro=1)

# Graficar
grafico_patron_elegido(capa_1, guardar_grafico=False)

# Generar puntos de código G
puntos_codigo_g(capa_1)

# Insertar en base de datos
insertar_en_sqlite3(capa_1, usuario="pepe", nombre="capa_1")
```

---

## Tabla de Equivalencias

| Método de Clase | Función Equivalente | Diferencia |
|-----------------|-------------------|-----------|
| `__init__(...)` | `crear_diccionario_capa(...)` | Retorna un diccionario en lugar de crear una instancia |
| `self.JSON()` | `guardar_json(capa)` | Debe pasarse el diccionario como parámetro |
| `self.obtener_parametros_iniciales()` | `calculos_iniciales(capa)` | Modifica el diccionario directamente |
| `self.generar_patrones()` | `generar_patrones(capa)` | Retorna `(patrones, listas_de_patrones)` |
| `self.seleccionar_patron(param)` | `seleccionar_patron(capa, patrones, listas, param)` | Requiere patrones y listas como parámetros |
| `self.graficar_patron_elegido(guardar)` | `grafico_patron_elegido(capa, guardar)` | Mismo funcionamiento |
| `self.generar_puntos_codigo_g()` | `puntos_codigo_g(capa)` | Mismo funcionamiento |
| `self.sqlite3(usuario, nombre)` | `insertar_en_sqlite3(capa, usuario, nombre)` | Mismo funcionamiento |
| `self.ejecutar(guardar, esquemas)` | Combinación manual de funciones | Debe ejecutarse paso a paso |

---

## Ventajas de la Nueva Aproximación

1. **Funciones Independientes**: No requiere crear instancias de clase
2. **Mayor Flexibilidad**: Cada paso puede customizarse independientemente
3. **Sin Importaciones Circulares**: Todas las funciones están contenidas en un solo módulo
4. **Más Funcional**: Estilo de programación más funcional y modular
5. **Fácil de Testear**: Cada función puede ser testeada de forma aislada

---

## Consideraciones Importantes

### 1. Acceso a Datos
**Antes**: `capa_1.diccionario_capa["NP"]`  
**Ahora**: `capa_1["NP"]`  
(El diccionario se accede directamente, no como atributo de instancia)

### 2. Retorno de Patrones
**Antes**: Los patrones se almacenaban internamente en `self.patrones`  
**Ahora**: Deben capturarse en variables:
```python
patrones, listas_de_patrones = generar_patrones_func(capa_1)
```

### 3. Modificación de Diccionario
Las funciones modifican el diccionario **por referencia**, por lo que los cambios se persisten:
```python
capa_1 = crear_diccionario_capa(...)
calculos_iniciales_func(capa_1)  # Modifica capa_1
print(capa_1["NP"])  # Ya contiene el valor calculado
```

---

## Ejemplo Completo Comparativo

### Con Clase
```python
from clase_capa import GeneradorPatrones

capa = GeneradorPatrones(alfa=45, diametro_mandril=100, longitud_util=550)
capa.ejecutar(False, False)
capa.seleccionar_patron(1)
capa.graficar_patron_elegido(False)
capa.generar_puntos_codigo_g()
capa.sqlite3("usuario", "nombre")
```

### Con Funciones
```python
from funcion_capa import *

capa = crear_diccionario_capa(alfa=45, diametro_mandril=100, longitud_util=550)
guardar_json(capa)
calculos_iniciales(capa)
patrones, listas = generar_patrones(capa)
seleccionar_patron(capa, patrones, listas, 1)
grafico_patron_elegido(capa, False)
puntos_codigo_g(capa)
insertar_en_sqlite3(capa, "usuario", "nombre")
```

---

## Notas Finales

- Todas las funciones están contenidas en `funcion_capa.py`
- No hay dependencias externas a otros módulos
- El diccionario es la estructura central de datos
- Las funciones son idempotentes cuando es aplicable
