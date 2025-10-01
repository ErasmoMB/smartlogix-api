# SmartLogix API - Sistema Completo de Gestión Académica

API REST completa para el parcial de Tecnologías Emergentes. Sistema de gestión de estudiantes, cursos y matrículas con integración completa a Google Cloud Platform.

## 🎯 Características del Sistema

- ✅ **API REST completa** con FastAPI
- ✅ **Base de datos en Cloud SQL** (PostgreSQL)
- ✅ **Todas las rutas requeridas** del parcial
- ✅ **Lógica de negocio implementada** (puntajes, estados)
- ✅ **Preparado para BigQuery** 
- ✅ **Deployment en Cloud Run**
- ✅ **Documentación automática** (Swagger/ReDoc)

## 📋 Endpoints Implementados

### Estudiantes
- `POST /students` → Registrar estudiante
- `GET /students` → Listar estudiantes
- `GET /students/{id}` → Obtener estudiante
- `GET /students/{id}/enrollments` → Cursos del estudiante

### Cursos
- `POST /courses` → Registrar curso
- `GET /courses` → Listar cursos  
- `GET /courses/{id}` → Obtener curso

### Matrículas
- `POST /enrollments` → Matricular estudiante (puntaje = 100)
- `PUT /enrollments/{id}` → Cambiar estado (ej. "Inactivo")
- `GET /enrollments` → Listar matrículas
- `GET /enrollments/{id}` → Obtener matrícula

### Sistema
- `GET /` → Información de la API
- `GET /health` → Estado de salud
- `GET /test` → Endpoint de pruebas

## 🚀 Deployment en Google Cloud

### 1. Configurar Cloud SQL

```bash
# 1. Crear instancia de Cloud SQL (PostgreSQL)
gcloud sql instances create smartlogix-instance \
    --database-version=POSTGRES_13 \
    --tier=db-f1-micro \
    --region=us-central1

# 2. Crear base de datos
gcloud sql databases create smartlogix_db \
    --instance=smartlogix-instance

# 3. Crear usuario
gcloud sql users create smartlogix_user \
    --instance=smartlogix-instance \
    --password=TU_PASSWORD_SEGURO

# 4. Ejecutar script SQL para crear tablas
gcloud sql connect smartlogix-instance --user=smartlogix_user
# Luego ejecutar el contenido de sql/create_tables.sql
```

### 2. Desplegar en Cloud Run

```bash
# 1. Configurar variables de entorno
export PROJECT_ID=tu-proyecto-gcp
export CLOUD_SQL_CONNECTION_NAME=${PROJECT_ID}:us-central1:smartlogix-instance

# 2. Deployment directo desde código
gcloud run deploy smartlogix-api \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8000 \
    --set-env-vars="CLOUD_SQL_CONNECTION_NAME=${CLOUD_SQL_CONNECTION_NAME}" \
    --set-env-vars="DB_USER=smartlogix_user" \
    --set-env-vars="DB_PASSWORD=TU_PASSWORD_SEGURO" \
    --set-env-vars="DB_NAME=smartlogix_db" \
    --add-cloudsql-instances ${CLOUD_SQL_CONNECTION_NAME}

# 3. Verificar deployment
gcloud run services describe smartlogix-api \
    --platform managed \
    --region us-central1 \
    --format 'value(status.url)'
```

### 3. Configurar BigQuery

```bash
# 1. Crear dataset
bq mk --dataset ${PROJECT_ID}:academy_dataset

# 2. Habilitar Data Transfer Service o crear Cloud Function
# para sincronizar datos de Cloud SQL a BigQuery

# 3. Crear tablas en BigQuery (misma estructura que Cloud SQL)
# 4. Ejecutar queries del archivo sql/bigquery_queries.sql
```

### 4. Dashboard en Looker Studio

1. Conectar Looker Studio a BigQuery
2. Seleccionar dataset `academy_dataset`
3. Crear gráficos según los queries proporcionados

## 🧪 Pruebas Locales

```bash
# 1. Clonar repositorio
git clone https://github.com/ErasmoMB/smartlogix-api.git
cd smartlogix-api

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# 4. Ejecutar aplicación
python main.py
```

La API estará disponible en `http://localhost:8000`

## 📖 Documentación API

- **Swagger UI**: `https://tu-url/docs`
- **ReDoc**: `https://tu-url/redoc`
- **OpenAPI Schema**: `https://tu-url/openapi.json`

## 🧪 Ejemplos de Uso

### Crear estudiante
```bash
curl -X POST https://tu-url/students \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "correo": "juan.perez@email.com"
  }'
```

### Crear curso
```bash
curl -X POST https://tu-url/courses \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Introducción a Python",
    "descripcion": "Curso básico de programación"
  }'
```

### Matricular estudiante
```bash
curl -X POST https://tu-url/enrollments \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "course_id": 1
  }'
```

### Cambiar estado a Inactivo
```bash
curl -X PUT https://tu-url/enrollments/1 \
  -H "Content-Type: application/json" \
  -d '{
    "estado": "Inactivo"
  }'
```

## 🏗️ Estructura del Proyecto

```
smartlogix-api/
├── app/
│   ├── models/
│   │   ├── models.py          # Modelos SQLAlchemy
│   │   └── schemas.py         # Esquemas Pydantic
│   ├── routes/
│   │   ├── students.py        # Rutas de estudiantes
│   │   ├── courses.py         # Rutas de cursos
│   │   └── enrollments.py     # Rutas de matrículas
│   └── database/
│       └── database.py        # Configuración de BD
├── sql/
│   ├── create_tables.sql      # Script de creación
│   └── bigquery_queries.sql   # Queries para BigQuery
├── main.py                    # Aplicación principal
├── requirements.txt           # Dependencias
├── Dockerfile                 # Contenedor
└── README.md                  # Esta documentación
```

## 🎨 Funcionalidad Emergente con IA (Propuesta)

### Predicción de Deserción con Vertex AI

Modelo de machine learning que predice la probabilidad de deserción de estudiantes basado en:
- Puntajes históricos
- Tiempo en el curso
- Patrones de actividad
- Comparación con cohortes similares

```python
# Integración con Vertex AI para predicción
@app.post("/predict/desertion")
async def predict_student_desertion(student_id: int):
    # Obtener datos del estudiante
    # Llamar modelo de Vertex AI
    # Retornar probabilidad de deserción
    pass
```

## � Métricas de BigQuery

El sistema incluye queries optimizadas para:
- Total de estudiantes activos por curso
- Promedio de puntaje por curso  
- Análisis de deserción
- Tendencias temporales
- Rankings de estudiantes

## ⚠️ Consideraciones de Producción

- Configurar SSL/TLS en Cloud SQL
- Implementar autenticación JWT
- Agregar rate limiting
- Configurar monitoring con Cloud Logging
- Implementar backup automático
- Configurar alertas de salud

## 🤝 Equipo de Desarrollo

- **[Tu Nombre]** - Desarrollo Full Stack
- **[Compañero 1]** - Base de datos y BigQuery
- **[Compañero 2]** - Frontend y Dashboard

---

**SmartLogix API v2.0** - Sistema completo para gestión académica online 🎓