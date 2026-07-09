from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from models.prolog_model import PrologModel
from controllers.rutas_controller import build_router

app = FastAPI(title="Rutas entre Ciudades - Guatemala")

model = PrologModel()

router = build_router(model)
app.include_router(router, prefix="/api")

app.mount("/static", StaticFiles(directory="views"), name="static")

@app.get("/")
def index():
    return FileResponse("views/index.html")