"""
Modelos SQLAlchemy para SmartLogix API
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(150), unique=True, nullable=False, index=True)
    fecha_registro = Column(DateTime, default=func.current_timestamp())
    
    # Relación con enrollments
    enrollments = relationship("Enrollment", back_populates="student")

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text)
    fecha_creacion = Column(DateTime, default=func.current_timestamp())
    
    # Relación con enrollments
    enrollments = relationship("Enrollment", back_populates="course")

class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    estado = Column(String(20), default="Activo")
    puntaje = Column(Integer, default=100)
    fecha_matricula = Column(DateTime, default=func.current_timestamp())
    
    # Relaciones
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")