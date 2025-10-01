"""
Rutas para gestión de matrículas (enrollments)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.database import get_db
from app.models.models import Enrollment, Student, Course
from app.models.schemas import EnrollmentCreate, EnrollmentUpdate, APIResponse

router = APIRouter(prefix="/enrollments", tags=["enrollments"])

@router.post("/", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def create_enrollment(enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    """Matricular estudiante en un curso (asigna puntaje = 100)"""
    
    # Verificar que el estudiante existe
    student = db.query(Student).filter(Student.id == enrollment.student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    # Verificar que el curso existe
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado"
        )
    
    # Verificar si ya está matriculado
    existing_enrollment = db.query(Enrollment).filter(
        Enrollment.student_id == enrollment.student_id,
        Enrollment.course_id == enrollment.course_id
    ).first()
    
    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El estudiante ya está matriculado en este curso"
        )
    
    # Crear nueva matrícula con puntaje inicial = 100
    db_enrollment = Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
        estado="Activo",
        puntaje=100  # Regla de negocio: puntaje inicial = 100
    )
    
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    
    # 🚀 SINCRONIZAR AUTOMÁTICAMENTE A BIGQUERY
    try:
        import requests
        sync_response = requests.post("https://smartlogix-api-250805843264.us-central1.run.app/sync/bigquery", timeout=10)
        print(f"🔄 Sincronización automática: {sync_response.status_code}")
    except Exception as e:
        print(f"⚠️ Error en sincronización automática: {e}")
    
    return APIResponse(
        message="Estudiante matriculado exitosamente",
        data={
            "enrollment_id": db_enrollment.id,
            "student": {
                "id": student.id,
                "nombre": student.nombre,
                "correo": student.correo
            },
            "course": {
                "id": course.id,
                "titulo": course.titulo,
                "descripcion": course.descripcion
            },
            "estado": db_enrollment.estado,
            "puntaje": db_enrollment.puntaje,
            "fecha_matricula": db_enrollment.fecha_matricula.isoformat()
        }
    )

@router.put("/{enrollment_id}", response_model=APIResponse)
async def update_enrollment(enrollment_id: int, enrollment_update: EnrollmentUpdate, db: Session = Depends(get_db)):
    """Cambiar estado de matrícula (ej. a 'Inactivo')"""
    
    # Buscar la matrícula
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matrícula no encontrada"
        )
    
    # Validar estados permitidos
    valid_states = ["Activo", "Inactivo", "Completado", "Abandonado"]
    if enrollment_update.estado not in valid_states:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Estado no válido. Estados permitidos: {', '.join(valid_states)}"
        )
    
    # Actualizar estado
    old_estado = enrollment.estado
    enrollment.estado = enrollment_update.estado
    
    db.commit()
    db.refresh(enrollment)
    
    # Obtener información del estudiante y curso para la respuesta
    student = db.query(Student).filter(Student.id == enrollment.student_id).first()
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    
    return APIResponse(
        message=f"Estado de matrícula actualizado de '{old_estado}' a '{enrollment_update.estado}'",
        data={
            "enrollment_id": enrollment.id,
            "student": {
                "id": student.id,
                "nombre": student.nombre,
                "correo": student.correo
            },
            "course": {
                "id": course.id,
                "titulo": course.titulo
            },
            "estado_anterior": old_estado,
            "estado_actual": enrollment.estado,
            "puntaje": enrollment.puntaje,
            "fecha_matricula": enrollment.fecha_matricula.isoformat()
        }
    )

@router.get("/", response_model=APIResponse)
async def get_enrollments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de todas las matrículas"""
    try:
        enrollments = db.query(Enrollment, Student, Course).join(
            Student, Enrollment.student_id == Student.id
        ).join(
            Course, Enrollment.course_id == Course.id
        ).offset(skip).limit(limit).all()
        
        enrollments_data = []
        for enrollment, student, course in enrollments:
            enrollments_data.append({
                "enrollment_id": enrollment.id,
                "student": {
                    "id": student.id,
                    "nombre": student.nombre,
                    "correo": student.correo
                },
                "course": {
                    "id": course.id,
                    "titulo": course.titulo,
                    "descripcion": course.descripcion
                },
                "estado": enrollment.estado,
                "puntaje": enrollment.puntaje,
                "fecha_matricula": enrollment.fecha_matricula.isoformat()
            })
        
        return APIResponse(
            message="Lista de matrículas obtenida exitosamente",
            data=enrollments_data,
            total=len(enrollments_data)
        )
    except Exception as e:
        print(f"Error en get_enrollments: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener matrículas: {str(e)}"
        )

@router.get("/{enrollment_id}", response_model=APIResponse)
async def get_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    """Obtener una matrícula específica por ID"""
    enrollment = db.query(Enrollment, Student, Course).join(
        Student, Enrollment.student_id == Student.id
    ).join(
        Course, Enrollment.course_id == Course.id
    ).filter(Enrollment.id == enrollment_id).first()
    
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matrícula no encontrada"
        )
    
    enrollment_obj, student, course = enrollment
    
    return APIResponse(
        message="Matrícula obtenida exitosamente",
        data={
            "enrollment_id": enrollment_obj.id,
            "student": {
                "id": student.id,
                "nombre": student.nombre,
                "correo": student.correo
            },
            "course": {
                "id": course.id,
                "titulo": course.titulo,
                "descripcion": course.descripcion
            },
            "estado": enrollment_obj.estado,
            "puntaje": enrollment_obj.puntaje,
            "fecha_matricula": enrollment_obj.fecha_matricula.isoformat()
        }
    )