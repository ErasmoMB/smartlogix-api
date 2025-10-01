from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os
from app.routes import students, courses, enrollments
from app.database.database import init_database
from app.models.schemas import HealthResponse, APIResponse

app = FastAPI(
    title="SmartLogix API",
    description="API REST para gestión de estudiantes y cursos online - Sistema completo",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router)
app.include_router(courses.router)
app.include_router(enrollments.router)

from app.routes import sync
app.include_router(sync.router)

from app.routes import ai_success_predictor
app.include_router(ai_success_predictor.router, prefix="/ai", tags=["🧠 AI Success Predictor - Datos Reales"])

@app.get("/", response_model=APIResponse)
async def root():
    return APIResponse(
        message="¡Bienvenido a SmartLogix API!",
        data={
            "version": "2.0.0",
            "status": "API funcionando correctamente",
            "timestamp": datetime.now().isoformat(),
            "endpoints": {
                "students": "/students",
                "courses": "/courses", 
                "enrollments": "/enrollments",
                "health": "/health",
                "docs": "/docs"
            },
            "features": [
                "Gestión completa de estudiantes",
                "Gestión completa de cursos",
                "Sistema de matrículas con puntajes",
                "Estados de matrícula (Activo/Inactivo)",
                "Integración con Cloud SQL",
                "Preparado para BigQuery"
            ]
        }
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        message="SmartLogix API está funcionando correctamente",
        version="2.0.0"
    )

@app.get("/test", response_model=APIResponse)
async def test_endpoint():
    return APIResponse(
        message="¡Prueba exitosa!",
        data={
            "test_status": "OK",
            "environment": os.environ.get("ENVIRONMENT", "development"),
            "port": os.environ.get("PORT", "8000"),
            "database_configured": True,
            "timestamp": datetime.now().isoformat(),
            "cloud_sql_connection": os.environ.get("CLOUD_SQL_CONNECTION_NAME", "Not configured")
        }
    )

@app.on_event("startup")
async def startup_event():
    print("Iniciando SmartLogix API...")
    success = init_database()
    if success:
        print("SmartLogix API iniciada correctamente")
    else:
        print("SmartLogix API iniciada con advertencias de base de datos")

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False  
    )
