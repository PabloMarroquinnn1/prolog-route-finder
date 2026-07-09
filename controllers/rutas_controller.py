from fastapi import APIRouter
from models.prolog_model import PrologModel

def build_router(model: PrologModel) -> APIRouter:
    router = APIRouter()

    @router.get("/ciudades")
    def obtener_ciudades():
        try:
            ciudades = model.obtener_ciudades()
            return {"ciudades": ciudades}
        except Exception as e:
            return {"codigo": 500, "error": f"Error al obtener ciudades: {str(e)}"}

    @router.get("/ruta-corta/{origen}/{destino}")
    def ruta_mas_corta(origen: str, destino: str):
        try:
            origen = origen.strip().lower()
            destino = destino.strip().lower()
            if origen == destino:
                return {"codigo": 400, "error": "El origen y destino no pueden ser iguales"}
            resultado = model.obtener_ruta_mas_corta(origen, destino)
            if resultado:
                return {"codigo": 200, "resultado": resultado}
            return {"codigo": 404, "error": "No existe ruta entre esas ciudades"}
        except Exception as e:
            return {"codigo": 500, "error": f"Error al calcular ruta: {str(e)}"}

    @router.get("/todas-rutas/{origen}/{destino}")
    def todas_las_rutas(origen: str, destino: str):
        try:
            origen = origen.strip().lower()
            destino = destino.strip().lower()
            if origen == destino:
                return {"codigo": 400, "error": "El origen y destino no pueden ser iguales"}
            rutas = model.obtener_todas_rutas(origen, destino)
            if rutas:
                return {"codigo": 200, "rutas": rutas}
            return {"codigo": 404, "error": "No existe ruta entre esas ciudades"}
        except Exception as e:
            return {"codigo": 500, "error": f"Error al obtener rutas: {str(e)}"}

    @router.post("/agregar-ciudad")
    def agregar_ciudad(nombre: str):
        try:
            nombre = nombre.strip().lower().replace(" ", "")
            if not nombre:
                return {"codigo": 400, "error": "El nombre no puede estar vacio"}
            if not nombre.isalpha():
                return {"codigo": 400, "error": "El nombre solo puede contener letras sin espacios ni tildes"}
            if len(nombre) < 3:
                return {"codigo": 400, "error": "El nombre debe tener al menos 3 letras"}
            ciudades_existentes = model.obtener_ciudades()
            if nombre in ciudades_existentes:
                return {"codigo": 400, "error": f"La ciudad {nombre.capitalize()} ya existe"}
            model.agregar_ciudad(nombre)
            return {"codigo": 200, "mensaje": f"Ciudad {nombre.capitalize()} agregada exitosamente"}
        except Exception as e:
            return {"codigo": 500, "error": f"Error al agregar ciudad: {str(e)}"}

    @router.post("/agregar-conexion")
    def agregar_conexion(origen: str, destino: str, distancia: int):
        try:
            origen = origen.strip().lower()
            destino = destino.strip().lower()
            if not origen or not destino:
                return {"codigo": 400, "error": "El origen y destino no pueden estar vacios"}
            if origen == destino:
                return {"codigo": 400, "error": "El origen y destino no pueden ser iguales"}
            if distancia <= 0:
                return {"codigo": 400, "error": "La distancia debe ser mayor a 0"}
            ciudades_existentes = model.obtener_ciudades()
            if origen not in ciudades_existentes:
                return {"codigo": 400, "error": f"La ciudad {origen.capitalize()} no existe en la base de conocimiento"}
            if destino not in ciudades_existentes:
                return {"codigo": 400, "error": f"La ciudad {destino.capitalize()} no existe en la base de conocimiento"}
            if model.existe_conexion(origen, destino):
                return {"codigo": 400, "error": f"Ya existe una conexion entre {origen.capitalize()} y {destino.capitalize()}"}
            model.agregar_conexion(origen, destino, distancia)
            return {"codigo": 200, "mensaje": f"Conexion {origen.capitalize()} - {destino.capitalize()} ({distancia} km) agregada exitosamente"}
        except Exception as e:
            return {"codigo": 500, "error": f"Error al agregar conexion: {str(e)}"}

    return router