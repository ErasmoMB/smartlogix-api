"""
Script para generar datos de prueba en SmartLogix API
Crea estudiantes, cursos y matrículas simuladas
"""
import requests
import json
import time
from datetime import datetime

# URL de tu API
API_BASE = "https://smartlogix-api-250805843264.us-central1.run.app"

def crear_datos_prueba():
    print("🚀 Generando datos de prueba para SmartLogix...")
    
    # 1. Crear estudiantes
    estudiantes = [
        {"nombre": "Juan Pérez", "correo": "juan.perez@email.com"},
        {"nombre": "María García", "correo": "maria.garcia@email.com"},
        {"nombre": "Carlos López", "correo": "carlos.lopez@email.com"},
        {"nombre": "Ana Martínez", "correo": "ana.martinez@email.com"},
        {"nombre": "Luis Rodríguez", "correo": "luis.rodriguez@email.com"},
        {"nombre": "Sofia Hernández", "correo": "sofia.hernandez@email.com"},
        {"nombre": "Diego Torres", "correo": "diego.torres@email.com"},
        {"nombre": "Laura Sánchez", "correo": "laura.sanchez@email.com"}
    ]
    
    print("👥 Creando estudiantes...")
    estudiantes_creados = []
    for estudiante in estudiantes:
        try:
            response = requests.post(f"{API_BASE}/students/", json=estudiante)
            if response.status_code == 201:
                data = response.json()
                estudiantes_creados.append(data['data']['id'])
                print(f"✅ Estudiante creado: {estudiante['nombre']}")
            else:
                print(f"❌ Error creando {estudiante['nombre']}: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
        time.sleep(0.5)
    
    # 2. Crear cursos
    cursos = [
        {"titulo": "Introducción a Python", "descripcion": "Curso básico de programación en Python"},
        {"titulo": "JavaScript Avanzado", "descripcion": "Conceptos avanzados de JavaScript y frameworks"},
        {"titulo": "Bases de Datos", "descripcion": "Diseño y gestión de bases de datos relacionales"},
        {"titulo": "Machine Learning", "descripcion": "Introducción al aprendizaje automático"},
        {"titulo": "Cloud Computing", "descripcion": "Servicios en la nube con Google Cloud Platform"}
    ]
    
    print("\n📚 Creando cursos...")
    cursos_creados = []
    for curso in cursos:
        try:
            response = requests.post(f"{API_BASE}/courses/", json=curso)
            if response.status_code == 201:
                data = response.json()
                cursos_creados.append(data['data']['id'])
                print(f"✅ Curso creado: {curso['titulo']}")
            else:
                print(f"❌ Error creando {curso['titulo']}: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
        time.sleep(0.5)
    
    # 3. Crear matrículas
    print("\n📝 Creando matrículas...")
    matriculas = [
        # Estudiante 1 en múltiples cursos
        {"student_id": 1, "course_id": 1}, # Juan en Python
        {"student_id": 1, "course_id": 2}, # Juan en JavaScript
        {"student_id": 1, "course_id": 3}, # Juan en BD
        
        # Estudiante 2
        {"student_id": 2, "course_id": 1}, # María en Python
        {"student_id": 2, "course_id": 4}, # María en ML
        
        # Estudiante 3
        {"student_id": 3, "course_id": 2}, # Carlos en JavaScript
        {"student_id": 3, "course_id": 5}, # Carlos en Cloud
        
        # Estudiante 4
        {"student_id": 4, "course_id": 1}, # Ana en Python
        {"student_id": 4, "course_id": 3}, # Ana en BD
        {"student_id": 4, "course_id": 4}, # Ana en ML
        
        # Estudiante 5
        {"student_id": 5, "course_id": 5}, # Luis en Cloud
        {"student_id": 5, "course_id": 1}, # Luis en Python
        
        # Más estudiantes
        {"student_id": 6, "course_id": 2}, # Sofia en JavaScript
        {"student_id": 6, "course_id": 4}, # Sofia en ML
        
        {"student_id": 7, "course_id": 3}, # Diego en BD
        {"student_id": 7, "course_id": 5}, # Diego en Cloud
        
        {"student_id": 8, "course_id": 1}, # Laura en Python
        {"student_id": 8, "course_id": 4}, # Laura en ML
    ]
    
    matriculas_creadas = []
    for matricula in matriculas:
        try:
            response = requests.post(f"{API_BASE}/enrollments/", json=matricula)
            if response.status_code == 201:
                data = response.json()
                matriculas_creadas.append(data['data']['enrollment_id'])
                print(f"✅ Matrícula creada: Estudiante {matricula['student_id']} en Curso {matricula['course_id']}")
            else:
                print(f"❌ Error en matrícula: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
        time.sleep(0.5)
    
    # 4. Marcar algunas matrículas como inactivas
    print("\n🔄 Marcando algunas matrículas como inactivas...")
    matriculas_inactivas = [2, 5, 8]  # IDs de matrículas a desactivar
    
    for matricula_id in matriculas_inactivas:
        try:
            response = requests.put(f"{API_BASE}/enrollments/{matricula_id}", 
                                  json={"estado": "Inactivo"})
            if response.status_code == 200:
                print(f"✅ Matrícula {matricula_id} marcada como Inactiva")
            else:
                print(f"❌ Error marcando matrícula {matricula_id}: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
        time.sleep(0.5)
    
    print("\n🎉 ¡Datos de prueba creados exitosamente!")
    print(f"📊 Estudiantes: {len(estudiantes_creados)}")
    print(f"📚 Cursos: {len(cursos_creados)}")
    print(f"📝 Matrículas: {len(matriculas_creadas)}")
    print("\n🌐 Verifica tu API en:")
    print(f"   {API_BASE}/students/")
    print(f"   {API_BASE}/courses/")
    print(f"   {API_BASE}/enrollments/")

if __name__ == "__main__":
    crear_datos_prueba()