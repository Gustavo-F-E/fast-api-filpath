import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Parámetros de la hélice
z = np.linspace(0, 4 * np.pi, 100)  # Dos vueltas completas
x = np.sin(z)
y = np.cos(z)

# Función para crear un rectángulo (3x1) con rotación
def create_rectangle(width, height, center, angle):
    # Coordenadas del rectángulo sin rotar
    x_rect = np.array([-width / 2, width / 2, width / 2, -width / 2, -width / 2])
    y_rect = np.array([-height / 2, -height / 2, height / 2, height / 2, -height / 2])
    z_rect = np.full_like(x_rect, center[2])

    # Matriz de rotación para el ángulo de la tangente
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)], 
                                [np.sin(angle), np.cos(angle)]])

    # Aplicar la rotación
    rotated_coords = np.dot(rotation_matrix, np.array([x_rect, y_rect]))

    # Trasladar las coordenadas a la posición correspondiente
    x_rot = rotated_coords[0, :] + center[0]
    y_rot = rotated_coords[1, :] + center[1]

    return np.array([x_rot, y_rot, z_rect]).T

# Crear las secciones (rectángulos) y la trayectoria
rectangles = []
for i in range(len(z)):
    # Calculamos el ángulo para mantener los lados paralelos al radio vector
    angle = np.arctan2(y[i], x[i])  # Ángulo respecto al eje X-Y
    rectangles.append(create_rectangle(3, 1, [x[i], y[i], z[i]], angle))

# **Primer gráfico: Mostrar el perfil (rectángulo) en 2D**
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
# Solo graficamos el primer rectángulo en 2D
ax1.plot(rectangles[0][:, 0], rectangles[0][:, 1], 'b-', alpha=0.7)
ax1.set_title('Perfil (Rectángulo) - 2D')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_aspect('equal')  # Para que el gráfico sea cuadrado
plt.show()

# **Segundo gráfico: Mostrar la trayectoria en 3D**
fig2 = plt.figure()
ax2 = fig2.add_subplot(111, projection='3d')
ax2.plot(x, y, z, 'r-', label="Trayectoria", linewidth=2)
ax2.set_title('Trayectoria (Hélice) - 3D')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
plt.show()

# **Tercer gráfico: Mostrar la extrusión en 3D con rotación de los rectángulos**
fig3 = plt.figure()
ax3 = fig3.add_subplot(111, projection='3d')

# Graficar las secciones y líneas entre ellas
for i in range(len(rectangles)):
    ax3.plot(rectangles[i][:, 0], rectangles[i][:, 1], rectangles[i][:, 2], 'b-', alpha=0.7)

# Conectar las secciones para mostrar la extrusión
for i in range(1, len(rectangles)):
    for j in range(len(rectangles[0])):
        ax3.plot([rectangles[i-1][j, 0], rectangles[i][j, 0]],
                [rectangles[i-1][j, 1], rectangles[i][j, 1]],
                [rectangles[i-1][j, 2], rectangles[i][j, 2]], 'k-', alpha=0.5)

ax3.set_title('Extrusión con rotación - 3D')
ax3.set_xlabel('X')
ax3.set_ylabel('Y')
ax3.set_zlabel('Z')
plt.show()
