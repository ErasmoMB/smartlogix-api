import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from app.models.models import Base

class DatabaseConfig:
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres123")
    DB_NAME = os.getenv("DB_NAME", "smartlogix_db")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    
    CLOUD_SQL_CONNECTION_NAME = os.getenv("CLOUD_SQL_CONNECTION_NAME")
    
    @classmethod
    def get_database_url(cls) -> str:
        if cls.CLOUD_SQL_CONNECTION_NAME:
            return f"postgresql+psycopg2://{cls.DB_USER}:{cls.DB_PASSWORD}@/{cls.DB_NAME}?host=/cloudsql/{cls.CLOUD_SQL_CONNECTION_NAME}"
        else:
            return f"postgresql+psycopg2://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"

def create_database_engine():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        database_url = DatabaseConfig.get_database_url()
    
    print(f"🔗 Conectando a: {database_url.replace(DatabaseConfig.DB_PASSWORD, '***')}")
    
    engine = create_engine(
        database_url,
        poolclass=NullPool,  
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False  
    )
    return engine

engine = create_database_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    try:
        create_tables()
        print("Base de datos inicializada correctamente")
        return True
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        return False