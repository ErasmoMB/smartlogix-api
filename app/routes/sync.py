"""
Endpoint para sincronización automática Cloud SQL → BigQuery
Se ejecuta después de cada operación CRUD
"""
import requests
import os
from fastapi import APIRouter, HTTPException
from google.cloud import bigquery
from datetime import datetime

router = APIRouter(prefix="/sync", tags=["sync"])

PROJECT_ID = "clever-gadget-471116-m6"
DATASET_ID = "academy_dataset"

def sync_table_to_bigquery(table_name: str, data: list):
    """Sincronizar una tabla específica a BigQuery usando TRUNCATE para evitar streaming buffer"""
    try:
        print(f"🔄 Iniciando sincronización de {table_name} con {len(data)} registros")
        
        # Configurar cliente BigQuery con región US
        client = bigquery.Client(project=PROJECT_ID, location="US")
        
        if not data:
            print(f"⚠️ No hay datos para {table_name}")
            return True
        
        # Usar TRUNCATE en lugar de DELETE para evitar problemas de streaming buffer
        try:
            truncate_query = f"TRUNCATE TABLE `{PROJECT_ID}.{DATASET_ID}.{table_name}`"
            client.query(truncate_query).result()
            print(f"🗑️ Tabla {table_name} truncada exitosamente")
        except Exception as truncate_error:
            print(f"⚠️ TRUNCATE falló: {truncate_error}")
            print(f"🔄 Intentando con DELETE (puede fallar por streaming buffer)")
            try:
                delete_query = f"DELETE FROM `{PROJECT_ID}.{DATASET_ID}.{table_name}` WHERE TRUE"
                client.query(delete_query).result()
                print(f"🗑️ DELETE exitoso para {table_name}")
            except Exception as delete_error:
                print(f"❌ DELETE también falló: {delete_error}")
                print(f"⚠️ Continuando con inserción (pueden haber duplicados)")
        
        # Insertar todos los datos de una vez
        table_ref = client.dataset(DATASET_ID).table(table_name)
        print(f"📥 Insertando {len(data)} registros en {table_name}")
        
        errors = client.insert_rows_json(table_ref, data)
        
        if errors:
            print(f"❌ Errores en {table_name}: {errors}")
            
            # Mostrar algunos errores para debugging
            for i, error in enumerate(errors[:5]):  # Solo primeros 5 errores
                print(f"   Error {i+1}: {error}")
            
            if len(errors) < len(data):
                print(f"⚠️ Inserción parcial: {len(data) - len(errors)}/{len(data)} registros exitosos")
                return False
            else:
                print(f"❌ Falló completamente la inserción")
                return False
        else:
            print(f"✅ {table_name}: {len(data)} registros sincronizados exitosamente")
            return True
            
    except Exception as e:
        print(f"❌ Error general sincronizando {table_name}: {e}")
        return False

@router.post("/bigquery")
async def sync_all_to_bigquery():
    """Sincronizar todas las tablas de Cloud SQL a BigQuery"""
    try:
        # Importar aquí para evitar dependencias circulares
        from app.database.database import get_db
        from app.models.models import Student, Course, Enrollment
        
        db = next(get_db())
        
        # Obtener todos los datos de Cloud SQL
        students = db.query(Student).all()
        courses = db.query(Course).all()
        enrollments = db.query(Enrollment).all()
        
        # Formatear datos para BigQuery
        students_data = [
            {
                'id': s.id,
                'nombre': s.nombre,
                'correo': s.correo,
                'fecha_registro': s.fecha_registro.isoformat() if s.fecha_registro else None
            }
            for s in students
        ]
        
        courses_data = [
            {
                'id': c.id,
                'titulo': c.titulo,
                'descripcion': c.descripcion or '',
                'fecha_creacion': c.fecha_creacion.isoformat() if c.fecha_creacion else None
            }
            for c in courses
        ]
        
        enrollments_data = [
            {
                'id': e.id,
                'student_id': e.student_id,
                'course_id': e.course_id,
                'estado': e.estado,
                'puntaje': e.puntaje,
                'fecha_matricula': e.fecha_matricula.isoformat() if e.fecha_matricula else None
            }
            for e in enrollments
        ]
        
        # Sincronizar cada tabla
        sync_results = {
            'students': sync_table_to_bigquery('students', students_data),
            'courses': sync_table_to_bigquery('courses', courses_data),
            'enrollments': sync_table_to_bigquery('enrollments', enrollments_data)
        }
        
        db.close()
        
        return {
            "message": "Sincronización completada",
            "timestamp": datetime.now().isoformat(),
            "results": sync_results,
            "counts": {
                "students": len(students_data),
                "courses": len(courses_data),
                "enrollments": len(enrollments_data)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en sincronización: {str(e)}")

@router.get("/status")
async def sync_status():
    """Verificar estado de sincronización"""
    try:
        # Configurar cliente BigQuery con región US
        client = bigquery.Client(project=PROJECT_ID, location="US")
        
        # Contar registros en BigQuery
        counts = {}
        for table in ['students', 'courses', 'enrollments']:
            query = f"SELECT COUNT(*) as total FROM `{PROJECT_ID}.{DATASET_ID}.{table}`"
            result = client.query(query).result()
            counts[table] = list(result)[0].total
        
        return {
            "status": "connected",
            "bigquery_counts": counts,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }