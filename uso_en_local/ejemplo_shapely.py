from shapely.geometry import Polygon, MultiPolygon
import matplotlib.pyplot as plt
from shapely.plotting import plot_polygon

# Definir puntos para cada área
area1_points = [(1, 1), (4, 1), (4, 4), (1, 4)]
area2_points = [(2, 2), (5, 2), (5, 5), (2, 5)]

# Crear polígonos usando Shapely
area1 = Polygon(area1_points)
area2 = Polygon(area2_points)

# Operaciones geométricas
union = area1.union(area2)            # Unión de áreas
intersection = area1.intersection(area2)  # Intersección de áreas
difference = area1.difference(area2)      # Diferencia (área1 - área2)
symmetric_difference = area1.symmetric_difference(area2)  # Diferencia simétrica

# Mostrar resultados
print("Unión:", union)
print("Intersección:", intersection)
print("Diferencia:", difference)
print("Diferencia Simétrica:", symmetric_difference)

# Función para dibujar el polígono o multipolígono
# Función para dibujar una lista de áreas
# Función para dibujar una lista de áreas con bordes negros y colores personalizados
def plot_areas(polygons, labels, colors):
    fig, ax = plt.subplots()  # Crear una nueva figura y ejes

    for polygon, label, color in zip(polygons, labels, colors):
        if isinstance(polygon, MultiPolygon):
            # Iterar sobre cada polígono en el MultiPolygon
            for poly in polygon.geoms:
                x, y = poly.exterior.xy
                ax.fill(x, y, alpha=0.5, color=color, edgecolor='black', linewidth=1, label=label)
            label = None  # Evitar duplicar etiquetas en la leyenda
        else:
            # Si es un solo Polygon, graficarlo directamente
            x, y = polygon.exterior.xy
            ax.fill(x, y, alpha=0.5, color=color, edgecolor='black', linewidth=1, label=label)
    
    ax.legend()
    plt.show()

# Lista de áreas y etiquetas para graficar
areas = [area1, area2, intersection, union, difference, symmetric_difference]
labels = ['Área 1', 'Área 2', 'Intersección', 'Unión', 'Diferencia', 'Diferencia Simétrica']
colors = ['blue', 'green', 'red', 'orange', 'purple', 'yellow']

# Llamada a la función para graficar todas las áreas en la misma figura
plot_areas(areas, labels, colors)

areas2 = [area1, area2]
labels2 = ['Área 1', 'Área 2']
colors2 = ['blue', 'green']
plot_areas(areas2, labels2, colors2)


# Lista de áreas y etiquetas para graficar
areas3 = [intersection, symmetric_difference]
labels3 = ['Intersección','Diferencia Simétrica']
colors3 = ['blue']
plot_areas(areas3, labels3, colors3)

# Lista de áreas y etiquetas para graficar
areas4 = [ union]
labels4 = ['Unión']
colors4 = ['red']
plot_areas(areas4, labels4, colors4)
# Lista de áreas y etiquetas para graficar
areas5 = [ difference]
labels5 = ['Diferencia Area 1 - Area 2']
colors5 = ['orange']
plot_areas(areas5, labels5, colors5)