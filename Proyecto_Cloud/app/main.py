from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.infrastructure.database.database import init_db, wait_for_db
from app.interfaces.web.routes import router
import asyncio

app = FastAPI(title="Sistema de Empleados - Arquitectura Hexagonal", version="1.0.0")

# Configurar templates
templates = Jinja2Templates(directory="app/interfaces/web/templates")
app.state.templates = templates

# Incluir rutas
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    # Esperar a que la base de datos esté lista
    await wait_for_db()
    await init_db()

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("list.html", {"request": request})