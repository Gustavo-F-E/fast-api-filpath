#app.py

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import matplotlib.pyplot as plt
import os
from fastapi.middleware.cors import CORSMiddleware

from generate_plot import generate_plot as generate_plot_function
from download_plot import download_plot as download_plot_function
from pydantic import BaseModel
from generate_and_download_plot import generate_and_download_plot as generate_and_download_plot_function

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:3000", "https://pw-app-filament-winding.vercel.app"],  # Cambia esto si es necesario
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los encabezados
)

@app.get('/')
def hello_world():
    return "Hola Mundo"


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)

# Definir el esquema de datos para las coordenadas
class Coordinates(BaseModel):
    X: float
    Y: float
    Z: float

@app.post("/generate-plot/")
async def generate_plot(coords: Coordinates):
    return generate_plot_function(coords)

@app.get("/download-plot/")
async def download_plot(X: float, Y: float, Z: float):
    return download_plot_function(X, Y, Z)

@app.post("/generate-and-download-plot/")
async def generate_and_download_plot(coords: Coordinates):
    return generate_and_download_plot_function(coords)