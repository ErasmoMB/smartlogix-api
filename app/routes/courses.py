"""
Rutas para gestión de cursos
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.models.models import Course
from app.models.schemas import CourseCreate, CourseResponse, APIResponse

router = APIRouter(prefix="/courses", tags=["courses"])

@router.post("/", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo curso"""
    
    # Crear nuevo curso
    db_course = Course(
        titulo=course.titulo,
        descripcion=course.descripcion
    )
    
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    
    # 🚀 SINCRONIZAR AUTOMÁTICAMENTE A BIGQUERY
    try:
        import requests
        sync_response = requests.post("https://smartlogix-api-250805843264.us-central1.run.app/sync/bigquery", timeout=10)
        print(f"🔄 Sincronización automática: {sync_response.status_code}")
    except Exception as e:
        print(f"⚠️ Error en sincronización automática: {e}")
    
    return APIResponse(
        message="Curso registrado exitosamente",
        data={
            "id": db_course.id,
            "titulo": db_course.titulo,
            "descripcion": db_course.descripcion,
            "fecha_creacion": db_course.fecha_creacion.isoformat()
        }
    )

@router.get("/", response_model=APIResponse)
async def get_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de cursos"""
    courses = db.query(Course).offset(skip).limit(limit).all()
    total = db.query(Course).count()
    
    courses_data = []
    for course in courses:
        courses_data.append({
            "id": course.id,
            "titulo": course.titulo,
            "descripcion": course.descripcion,
            "fecha_creacion": course.fecha_creacion.isoformat()
        })
    
    return APIResponse(
        message="Lista de cursos obtenida exitosamente",
        data=courses_data,
        total=total
    )

@router.get("/{course_id}", response_model=APIResponse)
async def get_course(course_id: int, db: Session = Depends(get_db)):
    """Obtener un curso por ID"""
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado"
        )
    
    return APIResponse(
        message="Curso obtenido exitosamente",
        data={
            "id": course.id,
            "titulo": course.titulo,
            "descripcion": course.descripcion,
            "fecha_creacion": course.fecha_creacion.isoformat()
        }
    )