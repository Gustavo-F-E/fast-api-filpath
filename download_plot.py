import os
from fastapi import HTTPException
from fastapi.responses import FileResponse

def download_plot(X: float, Y: float, Z: float):
    try:
        # Nombre del archivo
        file_name = f"X={X}-Y={Y}-Z={Z}.png"
        file_path = os.path.join("imagenes", file_name)
        
        # Verificar si el archivo existe
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Imagen no encontrada")
        
        # Descargar el archivo
        return FileResponse(file_path, media_type='image/png', filename=file_name)
    
    except Exception as e:
        return {"error": str(e)}