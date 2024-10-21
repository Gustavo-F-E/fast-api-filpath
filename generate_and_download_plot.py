import io
import matplotlib.pyplot as plt
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

class Coordinates(BaseModel):
    X: float
    Y: float
    Z: float

def generate_and_download_plot(coords: Coordinates):
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
        
        # Guardar el gráfico en memoria
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)  # Cerrar la figura para liberar memoria

        # Nombre del archivo para la descarga
        file_name = f"X={coords.X}-Y={coords.Y}-Z={coords.Z}.png"

        # Devolver la imagen para que se descargue automáticamente
        return StreamingResponse(buf, media_type="image/png", headers={"Content-Disposition": f"attachment; filename={file_name}"})
    
    except Exception as e:
        return {"error": str(e)}
