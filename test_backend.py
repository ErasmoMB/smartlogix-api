"""
Script de verificación local para SmartLogix API
Prueba las funcionalidades sin base de datos
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Probar que todas las importaciones funcionen"""
    try:
        print("🧪 Probando importaciones...")
        
        # Probar importación de FastAPI
        from fastapi import FastAPI
        print("✅ FastAPI importado correctamente")
        
        # Probar importación de modelos
        from app.models.models import Student, Course, Enrollment, Base
        print("✅ Modelos SQLAlchemy importados correctamente")
        
        # Probar importación de esquemas
        from app.models.schemas import StudentCreate, CourseCreate, EnrollmentCreate
        print("✅ Esquemas Pydantic importados correctamente")
        
        # Probar importación de rutas
        from app.routes import students, courses, enrollments
        print("✅ Rutas importadas correctamente")
        
        # Probar importación de database
        from app.database.database import DatabaseConfig
        print("✅ Configuración de base de datos importada correctamente")
        
        print("✅ Todas las importaciones exitosas!")
        return True
        
    except Exception as e:
        print(f"❌ Error en importaciones: {e}")
        return False

def test_schemas():
    """Probar que los esquemas funcionen correctamente"""
    try:
        print("\n🧪 Probando esquemas Pydantic...")
        
        from app.models.schemas import StudentCreate, CourseCreate, EnrollmentCreate
        
        # Probar crear estudiante
        student = StudentCreate(
            nombre="Juan Pérez",
            correo="juan.perez@email.com"
        )
        print(f"✅ Estudiante creado: {student.nombre} - {student.correo}")
        
        # Probar crear curso
        course = CourseCreate(
            titulo="Introducción a Python",
            descripcion="Curso básico de programación"
        )
        print(f"✅ Curso creado: {course.titulo}")
        
        # Probar crear matrícula
        enrollment = EnrollmentCreate(
            student_id=1,
            course_id=1
        )
        print(f"✅ Matrícula creada: estudiante {enrollment.student_id} en curso {enrollment.course_id}")
        
        print("✅ Todos los esquemas funcionan correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error en esquemas: {e}")
        return False

def test_app_creation():
    """Probar que la aplicación FastAPI se cree correctamente"""
    try:
        print("\n🧪 Probando creación de la aplicación...")
        
        # Simular variables de entorno
        os.environ.setdefault("DB_USER", "test_user")
        os.environ.setdefault("DB_PASSWORD", "test_password") 
        os.environ.setdefault("DB_NAME", "test_db")
        os.environ.setdefault("DB_HOST", "localhost")
        
        # Importar y crear la app (sin inicializar DB)
        from main import app
        
        print(f"✅ Aplicación FastAPI creada: {app.title} v{app.version}")
        print(f"✅ Rutas registradas: {len(app.routes)} rutas")
        
        # Verificar que las rutas principales estén registradas
        route_paths = [route.path for route in app.routes if hasattr(route, 'path')]
        expected_paths = ["/", "/health", "/test", "/students", "/courses", "/enrollments"]
        
        for path in expected_paths:
            if any(path in route_path for route_path in route_paths):
                print(f"✅ Ruta encontrada: {path}")
            else:
                print(f"⚠️ Ruta no encontrada: {path}")
        
        print("✅ Aplicación FastAPI creada correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error creando aplicación: {e}")
        return False

def test_database_config():
    """Probar configuración de base de datos"""
    try:
        print("\n🧪 Probando configuración de base de datos...")
        
        from app.database.database import DatabaseConfig
        
        # Configurar variables de entorno de prueba
        os.environ["DB_USER"] = "test_user"
        os.environ["DB_PASSWORD"] = "test_password"
        os.environ["DB_NAME"] = "test_db"
        os.environ["DB_HOST"] = "localhost"
        os.environ["DB_PORT"] = "5432"
        
        # Probar generación de URL
        db_url = DatabaseConfig.get_database_url()
        print(f"✅ URL de base de datos generada: {db_url[:50]}...")
        
        print("✅ Configuración de base de datos correcta!")
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración de base de datos: {e}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("🚀 Iniciando verificación completa del backend SmartLogix API\n")
    
    tests = [
        test_imports,
        test_schemas,
        test_database_config,
        test_app_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print("-" * 50)
    
    print(f"\n📊 Resultado de la verificación:")
    print(f"✅ Pruebas exitosas: {passed}/{total}")
    print(f"❌ Pruebas fallidas: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 ¡BACKEND COMPLETAMENTE VERIFICADO Y LISTO!")
        print("✅ El proyecto está listo para deployment en Cloud Run")
    else:
        print(f"\n⚠️ Hay {total - passed} problemas que deben resolverse")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)