# Configuración de BigQuery para SmartLogix API
# Pasos para sincronizar Cloud SQL con BigQuery

## 1. Crear el Dataset en BigQuery

```bash
# Crear el dataset academy_dataset
bq mk --dataset --location=US tu-proyecto:academy_dataset

# Verificar que se creó correctamente
bq ls tu-proyecto:academy_dataset
```

## 2. Crear las tablas en BigQuery (misma estructura que Cloud SQL)

```sql
-- Ejecutar en BigQuery Console

-- Tabla students
CREATE TABLE `tu-proyecto.academy_dataset.students` (
  id INT64,
  nombre STRING,
  correo STRING,
  fecha_registro TIMESTAMP
);

-- Tabla courses  
CREATE TABLE `tu-proyecto.academy_dataset.courses` (
  id INT64,
  titulo STRING,
  descripcion STRING,
  fecha_creacion TIMESTAMP
);

-- Tabla enrollments
CREATE TABLE `tu-proyecto.academy_dataset.enrollments` (
  id INT64,
  student_id INT64,
  course_id INT64,
  estado STRING,
  puntaje INT64,
  fecha_matricula TIMESTAMP
);
```

## 3. Configurar Data Transfer Service (Opción Recomendada)

### Habilitar las APIs necesarias:
```bash
gcloud services enable bigquerydatatransfer.googleapis.com
gcloud services enable sqladmin.googleapis.com
```

### Crear transferencia programada:
```bash
# Transferencia para tabla students
bq mk --transfer_config \
  --project_id=tu-proyecto \
  --data_source=scheduled_query \
  --display_name="Sync Students to BigQuery" \
  --target_dataset=academy_dataset \
  --schedule="every 1 hours" \
  --params='{
    "query": "SELECT * FROM EXTERNAL_QUERY(\"projects/tu-proyecto/locations/us-central1/connections/smartlogix-connection\", \"SELECT * FROM students;\")",
    "destination_table_name_template": "students",
    "write_disposition": "WRITE_TRUNCATE"
  }'

# Transferencia para tabla courses
bq mk --transfer_config \
  --project_id=tu-proyecto \
  --data_source=scheduled_query \
  --display_name="Sync Courses to BigQuery" \
  --target_dataset=academy_dataset \
  --schedule="every 1 hours" \
  --params='{
    "query": "SELECT * FROM EXTERNAL_QUERY(\"projects/tu-proyecto/locations/us-central1/connections/smartlogix-connection\", \"SELECT * FROM courses;\")",
    "destination_table_name_template": "courses",
    "write_disposition": "WRITE_TRUNCATE"
  }'

# Transferencia para tabla enrollments  
bq mk --transfer_config \
  --project_id=tu-proyecto \
  --data_source=scheduled_query \
  --display_name="Sync Enrollments to BigQuery" \
  --target_dataset=academy_dataset \
  --schedule="every 1 hours" \
  --params='{
    "query": "SELECT * FROM EXTERNAL_QUERY(\"projects/tu-proyecto/locations/us-central1/connections/smartlogix-connection\", \"SELECT * FROM enrollments;\")",
    "destination_table_name_template": "enrollments", 
    "write_disposition": "WRITE_TRUNCATE"
  }'
```

## 4. Alternativa: Cloud Function para sincronización

Si prefieres usar Cloud Function en lugar de Data Transfer Service:

### Crear Cloud Function:
```python
# main.py para Cloud Function
import functions_framework
from google.cloud import bigquery
from google.cloud.sql.connector import Connector
import sqlalchemy
import os

@functions_framework.http
def sync_to_bigquery(request):
    """Cloud Function para sincronizar datos de Cloud SQL a BigQuery"""
    
    # Configuración
    PROJECT_ID = os.environ.get('PROJECT_ID')
    CLOUD_SQL_CONNECTION_NAME = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME')
    
    try:
        # Conectar a Cloud SQL
        connector = Connector()
        
        def getconn():
            conn = connector.connect(
                CLOUD_SQL_CONNECTION_NAME,
                "pg8000",
                user=DB_USER,
                password=DB_PASSWORD,
                db=DB_NAME,
            )
            return conn
        
        engine = sqlalchemy.create_engine(
            "postgresql+pg8000://",
            creator=getconn,
        )
        
        # Cliente BigQuery
        bq_client = bigquery.Client(project=PROJECT_ID)
        
        # Sincronizar cada tabla
        tables = ['students', 'courses', 'enrollments']
        
        for table in tables:
            # Leer de Cloud SQL
            with engine.connect() as conn:
                df = pd.read_sql(f"SELECT * FROM {table}", conn)
            
            # Escribir a BigQuery
            table_id = f"{PROJECT_ID}.academy_dataset.{table}"
            job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
            
            job = bq_client.load_table_from_dataframe(df, table_id, job_config=job_config)
            job.result()
            
        return {"status": "success", "message": "Data synchronized successfully"}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

### Desplegar Cloud Function:
```bash
gcloud functions deploy sync-smartlogix-data \
    --runtime python39 \
    --trigger-http \
    --allow-unauthenticated \
    --set-env-vars PROJECT_ID=tu-proyecto \
    --set-env-vars CLOUD_SQL_CONNECTION_NAME=tu-proyecto:us-central1:smartlogix-instance \
    --set-env-vars DB_USER=smartlogix_user \
    --set-env-vars DB_PASSWORD=tu-password \
    --set-env-vars DB_NAME=smartlogix_db
```

### Configurar Cloud Scheduler para ejecutar cada hora:
```bash
gcloud scheduler jobs create http sync-bigquery-job \
    --schedule="0 * * * *" \
    --uri="https://us-central1-tu-proyecto.cloudfunctions.net/sync-smartlogix-data" \
    --http-method=GET
```

## 5. Verificar sincronización

```sql
-- Verificar que los datos se están sincronizando
SELECT 
  table_name,
  row_count,
  TIMESTAMP_MILLIS(last_modified_time) as last_updated
FROM `tu-proyecto.academy_dataset.__TABLES__`;

-- Probar el query principal del parcial
SELECT 
  c.titulo,
  COUNTIF(e.estado = 'Activo') AS total_activos,
  AVG(e.puntaje) AS promedio_puntaje
FROM `tu-proyecto.academy_dataset.enrollments` e
JOIN `tu-proyecto.academy_dataset.courses` c ON e.course_id = c.id
GROUP BY c.titulo;
```

## Notas importantes:
- Reemplaza `tu-proyecto` con tu PROJECT_ID real
- La sincronización se ejecutará cada hora
- Los datos en BigQuery se actualizarán completamente (WRITE_TRUNCATE)
- Para producción, considera usar WRITE_APPEND con deduplicación