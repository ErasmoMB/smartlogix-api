"""
SmartLogix API - Sistema de gestión académica
API REST completa para administrar estudiantes, cursos y matrículas
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os

# Importar rutas
from app.routes import students, courses, enrollments
from app.database.database import init_database
from app.models.schemas import HealthResponse, APIResponse

# Crear la aplicación FastAPI
app = FastAPI(
    title="SmartLogix API",
    description="API REST para gestión de estudiantes y cursos online - Sistema completo",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para permitir requests desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(enrollments.router)

# Incluir ruta de sincronización
from app.routes import sync
app.include_router(sync.router)

# Incluir rutas de IA
from app.routes import ai_recommendations, ai_demo
app.include_router(ai_recommendations.router, prefix="/ai", tags=["AI & Machine Learning"])
app.include_router(ai_demo.router, prefix="/ai-demo", tags=["🤖 AI Demo - Funcionando 100%"])

# Rutas principales
@app.get("/", response_model=APIResponse)
async def root():
    """Ruta principal de bienvenida"""
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
    """Endpoint de salud para verificar que la API esté funcionando"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        message="SmartLogix API está funcionando correctamente",
        version="2.0.0"
    )

@app.get("/test", response_model=APIResponse)
async def test_endpoint():
    """Endpoint de prueba para verificar conectividad y configuración"""
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

# Evento de inicio de la aplicación
@app.on_event("startup")
async def startup_event():
    """Inicializar la base de datos al iniciar la aplicación"""
    print("🚀 Iniciando SmartLogix API...")
    success = init_database()
    if success:
        print("✅ SmartLogix API iniciada correctamente")
    else:
        print("⚠️ SmartLogix API iniciada con advertencias de base de datos")

# Configuración para Cloud Run
if __name__ == "__main__":
    import uvicorn
    
    # Cloud Run asigna automáticamente el puerto via la variable de entorno PORT
    port = int(os.environ.get("PORT", 8000))
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False  # Deshabilitado en producción
    )
