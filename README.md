# SmartLogix API

API REST completa para gestión de estudiantes y cursos con integración de IA y Google Cloud Platform.

## 🚀 Características

- **API REST** completa con FastAPI
- **Base de datos** Cloud SQL PostgreSQL
- **Sincronización** automática con BigQuery
- **IA integrada** para recomendaciones inteligentes
- **Despliegue** en Google Cloud Run
- **Dashboard** analytics en Looker Studio

## 📋 Endpoints Principales

### Estudiantes
- `GET /students/` - Listar estudiantes
- `POST /students/` - Crear estudiante
- `GET /students/{id}` - Obtener estudiante
- `PUT /students/{id}` - Actualizar estudiante
- `DELETE /students/{id}` - Eliminar estudiante

### Cursos
- `GET /courses/` - Listar cursos
- `POST /courses/` - Crear curso
- `GET /courses/{id}` - Obtener curso
- `PUT /courses/{id}` - Actualizar curso
- `DELETE /courses/{id}` - Eliminar curso

### Matrículas
- `GET /enrollments/` - Listar matrículas
- `POST /enrollments/` - Crear matrícula
- `DELETE /enrollments/{id}` - Eliminar matrícula

### Sincronización
- `POST /sync/all` - Sincronizar todo con BigQuery
- `GET /sync/status` - Estado de sincronización

### IA & Recomendaciones
- `GET /ai-demo/recommend/{student_id}` - Recomendaciones inteligentes
- `GET /ai-demo/analytics/{student_id}` - Analytics predictivo
- `GET /ai-demo/demo-all` - Demo completo de IA

## 🛠️ Instalación y Uso

### Requisitos
- Python 3.11+
- Google Cloud SDK
- Docker (opcional)

### Configuración local
```bash
# Crear entorno virtual
python -m venv env
env\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar API
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Despliegue en Cloud Run
```bash
# Construir y desplegar
gcloud run deploy smartlogix-api --source . --region us-central1
```

## 🌐 URLs de Producción

- **API:** https://smartlogix-api-250805843264.us-central1.run.app/
- **Documentación:** https://smartlogix-api-250805843264.us-central1.run.app/docs
- **Dashboard:** [Looker Studio Dashboard]

## 🔧 Tecnologías

- **Backend:** FastAPI, SQLAlchemy, PostgreSQL
- **Cloud:** Google Cloud Run, Cloud SQL, BigQuery
- **IA:** Motor de recomendaciones inteligente
- **Contenedores:** Docker
- **Analytics:** Looker Studio

## 📊 Base de Datos

### Modelos principales:
- **Student:** Gestión de estudiantes
- **Course:** Gestión de cursos  
- **Enrollment:** Gestión de matrículas

### Sincronización automática:
Los datos se sincronizan automáticamente con BigQuery para analytics avanzados.

## 🤖 IA Integrada

El sistema incluye un motor de IA que:
- Analiza perfiles de estudiantes
- Genera recomendaciones personalizadas de cursos
- Proporciona analytics predictivos
- Calcula scores de compatibilidad

---

**Desarrollado para Tecnologías Emergentes - SmartLogix Academy**