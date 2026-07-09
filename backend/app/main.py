from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import engine, Base
from app.models import models
from app.routes import auth, questions, categories, logs, config
from app.services.seed import seed_data

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SmartBot API", version="1.0.0")

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Incluir rutas
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(questions.router, prefix="/api/questions", tags=["questions"])
app.include_router(categories.router, prefix="/api/categories", tags=["categories"])
app.include_router(logs.router, prefix="/api/logs", tags=["logs"])
app.include_router(config.router, prefix="/api/config", tags=["config"])

# Ruta principal - Panel Admin
from fastapi import Request
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def admin_panel(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.on_event("startup")
async def startup_event():
    seed_data()