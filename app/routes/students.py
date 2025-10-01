"""
Rutas para gestión de estudiantes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.models.models import Student
from app.models.schemas import StudentCreate, StudentResponse, APIResponse

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo estudiante"""
    
    # Verificar si el correo ya existe
    existing_student = db.query(Student).filter(Student.correo == student.correo).first()
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado"
        )
    
    # Crear nuevo estudiante
    db_student = Student(
        nombre=student.nombre,
        correo=student.correo
    )
    
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    
    # 🚀 SINCRONIZAR AUTOMÁTICAMENTE A BIGQUERY
    try:
        import requests
        sync_response = requests.post("https://smartlogix-api-250805843264.us-central1.run.app/sync/bigquery", timeout=10)
        print(f"🔄 Sincronización automática: {sync_response.status_code}")
    except Exception as e:
        print(f"⚠️ Error en sincronización automática: {e}")
    
    return APIResponse(
        message="Estudiante registrado exitosamente",
        data={
            "id": db_student.id,
            "nombre": db_student.nombre,
            "correo": db_student.correo,
            "fecha_registro": db_student.fecha_registro.isoformat()
        }
    )

@router.get("/", response_model=APIResponse)
async def get_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de estudiantes"""
    try:
        students = db.query(Student).offset(skip).limit(limit).all()
        
        students_data = []
        for student in students:
            students_data.append({
                "id": student.id,
                "nombre": student.nombre,
                "correo": student.correo,
                "fecha_registro": student.fecha_registro.isoformat()
            })
        
        return APIResponse(
            message="Lista de estudiantes obtenida exitosamente",
            data=students_data,
            total=len(students_data)
        )
    except Exception as e:
        print(f"Error en get_students: {e}")
        return APIResponse(
            message="Error al obtener estudiantes",
            data=[],
            total=0
        )

@router.get("/{student_id}", response_model=APIResponse)
async def get_student(student_id: int, db: Session = Depends(get_db)):
    """Obtener un estudiante por ID"""
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    return APIResponse(
        message="Estudiante obtenido exitosamente",
        data={
            "id": student.id,
            "nombre": student.nombre,
            "correo": student.correo,
            "fecha_registro": student.fecha_registro.isoformat()
        }
    )

@router.get("/{student_id}/enrollments", response_model=APIResponse)
async def get_student_enrollments(student_id: int, db: Session = Depends(get_db)):
    """Listar cursos donde está matriculado un estudiante"""
    from app.models.models import Enrollment, Course
    
    # Verificar que el estudiante existe
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    # Obtener matrículas con información del curso
    enrollments = db.query(Enrollment, Course).join(
        Course, Enrollment.course_id == Course.id
    ).filter(Enrollment.student_id == student_id).all()
    
    enrollments_data = []
    for enrollment, course in enrollments:
        enrollments_data.append({
            "enrollment_id": enrollment.id,
            "course_id": course.id,
            "course_title": course.titulo,
            "course_description": course.descripcion,
            "estado": enrollment.estado,
            "puntaje": enrollment.puntaje,
            "fecha_matricula": enrollment.fecha_matricula.isoformat()
        })
    
    return APIResponse(
        message=f"Cursos del estudiante {student.nombre} obtenidos exitosamente",
        data={
            "student": {
                "id": student.id,
                "nombre": student.nombre,
                "correo": student.correo
            },
            "enrollments": enrollments_data
        },
        total=len(enrollments_data)
    )