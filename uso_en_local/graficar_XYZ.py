import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def graficar_XYZ(X, Y, Z, R, L):
    # Crear la figura y los ejes en 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Graficar el cilindro
    z_cilindro = np.linspace(0, L, 100)  # Coordenadas z para el cilindro (de 0 a L)
    theta = np.linspace(0, 2 * np.pi, 100)  # Ángulo theta (0 a 2*pi)
    theta_grid, z_grid = np.meshgrid(theta, z_cilindro)  # Crear la malla
    x_cilindro = R * np.cos(theta_grid)  # Coordenadas x para el cilindro
    y_cilindro = R * np.sin(theta_grid)  # Coordenadas y para el cilindro

    # Graficar la superficie del cilindro
    ax.plot_surface(x_cilindro, y_cilindro, z_grid, alpha=0.5, rstride=5, cstride=5, color='cyan')

    # Graficar la hélice con los datos proporcionados
    ax.plot(X, Y, Z, label='Hélice en el espacio', color='blue', linewidth=2)

    # Etiquetas de los ejes
    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    ax.set_zlabel('Eje Z')
    
    # Ajuste manual de la escala de los ejes
    delta_X=(X.max()-X.max())*1.1
    delta_Y=(Y.max()-Y.max())*1.1
    delta_Z=(Z.max()-Z.max())*1.1

    ax.set_xlim(X.max()+delta_X, X.min()-delta_X)
    ax.set_ylim(Y.max()+delta_Y, Y.min()-delta_Y)
    ax.set_zlim(Z.max()+delta_Z, Z.min()-delta_Z)

    # Mostrar leyenda y gráfica
    ax.legend()
    plt.show()
