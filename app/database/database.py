"""
Configuración de la base de datos para SmartLogix API
"""
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from app.models.models import Base

# Configuración de la base de datos
class DatabaseConfig:
    # Variables de entorno para Cloud SQL
    DB_USER = os.getenv("DB_USER", "smartlogix_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "smartlogix_password")
    DB_NAME = os.getenv("DB_NAME", "smartlogix_db")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    
    # Para Cloud SQL con conexión privada
    CLOUD_SQL_CONNECTION_NAME = os.getenv("CLOUD_SQL_CONNECTION_NAME")
    
    @classmethod
    def get_database_url(cls) -> str:
        """Construir URL de conexión según el entorno"""
        if cls.CLOUD_SQL_CONNECTION_NAME:
            # Conexión a Cloud SQL en producción
            return f"postgresql+psycopg2://{cls.DB_USER}:{cls.DB_PASSWORD}@/{cls.DB_NAME}?host=/cloudsql/{cls.CLOUD_SQL_CONNECTION_NAME}"
        else:
            # Conexión local o desarrollo
            return f"postgresql+psycopg2://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"

# Crear engine de SQLAlchemy
def create_database_engine():
    database_url = DatabaseConfig.get_database_url()
    
    # Configuración del engine para Cloud Run
    engine = create_engine(
        database_url,
        poolclass=NullPool,  # Recomendado para Cloud Run
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False  # Cambiar a True para debug
    )
    return engine

# Engine global
engine = create_database_engine()

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Crear todas las tablas en la base de datos"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency para obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Inicializar la base de datos"""
    try:
        # Crear tablas si no existen
        create_tables()
        print("✅ Base de datos inicializada correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        return False