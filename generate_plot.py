import os
import matplotlib.pyplot as plt
from fastapi import HTTPException
from pydantic import BaseModel

# Definir el esquema de datos para las coordenadas
class Coordinates(BaseModel):
    X: float
    Y: float
    Z: float

def generate_plot(coords: Coordinates):
    try:
        # Crear el gráfico
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        # Crear un punto en los ejes X, Y, Z
        ax.scatter([coords.X], [coords.Y], [coords.Z], c='r', marker='o')
        
        # Etiquetas de los ejes
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        
        # Nombre del archivo
        file_name = f"X={coords.X}-Y={coords.Y}-Z={coords.Z}.png"
        file_path = os.path.join("imagenes", file_name)
        
        # Guardar el gráfico como PNG
        plt.savefig(file_path)
        plt.close(fig)  # Cerrar la figura para liberar memoria
        
        return {"message": f"Imagen guardada como {file_name}"}
    
    except Exception as e:
        return {"error": str(e)}