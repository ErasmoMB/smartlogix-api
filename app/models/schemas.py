"""
Esquemas Pydantic para SmartLogix API
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# Esquemas para Student
class StudentBase(BaseModel):
    nombre: str
    correo: EmailStr

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int
    fecha_registro: datetime
    
    class Config:
        from_attributes = True

# Esquemas para Course
class CourseBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True

# Esquemas para Enrollment
class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentUpdate(BaseModel):
    estado: str

class EnrollmentResponse(EnrollmentBase):
    id: int
    estado: str
    puntaje: int
    fecha_matricula: datetime
    
    class Config:
        from_attributes = True

# Esquemas con relaciones
class StudentWithEnrollments(StudentResponse):
    enrollments: List[EnrollmentResponse] = []

class CourseWithEnrollments(CourseResponse):
    enrollments: List[EnrollmentResponse] = []

# Esquemas para respuestas de API
class APIResponse(BaseModel):
    message: str
    data: Optional[dict | list] = None
    total: Optional[int] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    message: str
    version: str