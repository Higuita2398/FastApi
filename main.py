from fastapi import FastAPI, HTTPException, Path 
from typing import List
import requests

app = FastAPI()

def obtener_imagen_relacionada(titulo: str):
    # Título de la experiencia
    titulo = titulo

    # Clave de API de Unsplash
    access_key = '_dHabfpwjzCduYk7D3gGNsSgW_knoKgj7p6kugyqBUg'

    # URL del endpoint del API
    url = 'https://api.unsplash.com/search/photos'

    # Parámetros de la solicitud
    params = {'query': titulo}

    # Encabezados de la solicitud con la clave de API
    headers = {'Authorization': f'Client-ID {access_key}'}

    # Realiza la solicitud al API de Unsplash
    response = requests.get(url, params=params, headers=headers)

    # Procesa la respuesta
    if response.status_code == 200:
        data = response.json()
        # Obtiene la URL de la primera imagen encontrada
        if data['results']:
            imagen_relacionada = data['results'][0]['urls']['regular']
            return imagen_relacionada
        else:
            return None
    else:
        # Si hay un error, retorna None
        return None

# Datos dummy para inicializar el API
experiencias = [
    {
        "id": 1,
        "titulo": "Experiencia 1",
        "descripcion": "Descripción de la Experiencia 1",
        "sala": 1,
        "imagen": "imagen1.jpg"
    },
    {
        "id": 2,
        "titulo": "Experiencia 2",
        "descripcion": "Descripción de la Experiencia 2",
        "sala": 2,
        "imagen": "imagen2.jpg"
    }
]

# Rutas del API

@app.get("/experiencias/", response_model=List[dict])
async def listar_experiencias():
    return experiencias

@app.post("/experiencias/", response_model=dict)
async def crear_experiencia(titulo: str, descripcion: str, sala: int):
    nueva_experiencia = {
        "id": len(experiencias) + 1,
        "titulo": titulo,
        "descripcion": descripcion,
        "sala": sala,
        "imagen": f"https://api.imagenes.com/{titulo}"  # Imaginario, debes modificar esta parte
    }
    experiencias.append(nueva_experiencia)
    return nueva_experiencia

@app.get("/experiencias/{experiencia_id}", response_model=dict)
async def obtener_experiencia(experiencia_id: int = Path(..., title="ID de la experiencia")):
    for exp in experiencias:
        if exp["id"] == experiencia_id:
            return exp
    raise HTTPException(status_code=404, detail="Experiencia no encontrada")

@app.put("/experiencias/{experiencia_id}", response_model=dict)
async def actualizar_experiencia(experiencia_id: int, titulo: str, descripcion: str, sala: int):
    for exp in experiencias:
        if exp["id"] == experiencia_id:
            exp.update({"titulo": titulo, "descripcion": descripcion, "sala": sala})
            exp["imagen"] = f"https://api.imagenes.com/{titulo}"  # Imaginario, debes modificar esta parte
            return exp
    raise HTTPException(status_code=404, detail="Experiencia no encontrada")

@app.delete("/experiencias/{experiencia_id}")
async def borrar_experiencia(experiencia_id: int):
    for i, exp in enumerate(experiencias):
        if exp["id"] == experiencia_id:
            del experiencias[i]
            return {"message": "Experiencia eliminada"}
    raise HTTPException(status_code=404, detail="Experiencia no encontrada")

@app.get("/experiencias/salas/{nombre}", response_model=List[dict])
async def experiencias_por_sala(nombre: int):
    return [exp for exp in experiencias if exp["sala"] == nombre]

@app.get("/experiencias/salas/{nombre}/imagen", response_model=dict)
async def obtener_imagen_relacionada_por_sala(nombre: int):
    experiencia = next((exp for exp in experiencias if exp["sala"] == nombre), None)
    if experiencia:
        imagen_relacionada = obtener_imagen_relacionada(experiencia["nombre"])
        if imagen_relacionada:
            return {"imagen_relacionada": imagen_relacionada}
        else:
            raise HTTPException(status_code=404, detail="No se encontró una imagen relacionada para esta experiencia.")
    else:
        raise HTTPException(status_code=404, detail="No se encontró la experiencia en la sala especificada.")

experiencias = [
    {"id": 1, "nombre": "Experiencia 1", "sala": 1},
    {"id": 2, "nombre": "Experiencia 2", "sala": 2},
    {"id": 3, "nombre": "Experiencia 3", "sala": 1}
]
