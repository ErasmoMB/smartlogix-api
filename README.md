# SmartLogix API

**Sistema completo de gestión académica** con **IA predictiva** y **arquitectura cloud-native**. Implementa un pipeline de datos **end-to-end** desde API REST hasta **machine learning**, utilizando **Google Cloud Platform** para escalabilidad empresarial.

## 📖 Documentación Completa

**[📄 Ver Documentación Técnica Completa (PDF)](./PARCIAL-ERASMO%20MONTUFAR.pdf)**

> 📋 **Contenido del documento:**
> - 🚀 **SmartLogix API** - Sistema REST con FastAPI desplegado en Cloud Run
> - 🗄️ **Base de Datos** - Cloud SQL PostgreSQL con 32 estudiantes, 11 cursos, 61 matriculaciones
> - 📊 **BigQuery** - Data Warehouse con sincronización automática en tiempo real
> - 🤖 **IA Academic Success Predictor** - Machine Learning con datos reales del backend
> - 🔄 **Pipeline Completo** - API → Cloud SQL → BigQuery → Looker Studio
> - 📈 **Dashboard** - Visualizaciones en tiempo real (0-20)

---

## 🎯 **Arquitectura del Sistema**

### **🏗️ Stack Tecnológico**
- **API**: FastAPI 2.0.0 + SQLAlchemy
- **Base de Datos**: Google Cloud SQL PostgreSQL 14
- **Data Warehouse**: Google BigQuery
- **IA/ML**: Academic Success Predictor con datos reales
- **Infraestructura**: Google Cloud Run (serverless)
- **Analytics**: Looker Studio Dashboard
- **Pipeline**: Sincronización automática tiempo real

### **🔄 Flujo de Datos**
```
API REST → Cloud SQL → BigQuery → Looker Studio
    ↓           ↓          ↓           ↓
  CRUD       Storage   Analytics     Dashboards
Operations   (32/11/61)  ML Ready   Real-time
```

## 🚀 **Características Principales**

### **✅ API REST Completa**
- **CRUD completo** para Students, Courses, Enrollments
- **Validaciones robustas** con Pydantic schemas
- **Documentación automática** Swagger/OpenAPI
- **CORS configurado** para integraciones frontend
- **Manejo de errores** centralizado y profesional

### **✅ Sistema Educativo**
- **Calificaciones 0-20** 
- **Estados académicos**: Cursando, Aprobado, Desaprobado, Retirado
- **Emails institucionales** @smartlogix.edu
- **Timestamps precisos** para auditoría completa

### **✅ Sincronización Tiempo Real**
- **Endpoint único**: `POST /sync/bigquery` sincroniza todo
- **Monitoreo**: `GET /sync/status` verifica estado
- **Procesamiento por lotes** optimizado para BigQuery
- **Manejo de errores** avanzado con reintentos

### **✅ IA Academic Success Predictor**
- **Búsqueda flexible**: ID, email o nombre
- **Análisis predictivo** basado en historial real
- **Probabilidades de éxito** por curso (85-95% precisión)
- **Recomendaciones personalizadas** con justificación
- **Google Cloud AI Platform** para procesamiento

## 📋 **Endpoints de Producción**

### **👥 Gestión de Estudiantes**
```http
GET    /students/              # Listar 32 estudiantes
POST   /students/              # Crear estudiante
GET    /students/{id}          # Obtener por ID
PUT    /students/{id}          # Actualizar estudiante
DELETE /students/{id}          # Eliminar estudiante
GET    /students/{id}/enrollments  # Matriculaciones del estudiante
```

### **📚 Gestión de Cursos**
```http
GET    /courses/               # Listar 11 cursos tecnológicos
POST   /courses/               # Crear curso
GET    /courses/{id}           # Obtener por ID  
PUT    /courses/{id}           # Actualizar curso
DELETE /courses/{id}          # Eliminar curso
```

### **📝 Gestión de Matriculaciones**
```http
GET    /enrollments/           # Listar 61 matriculaciones
POST   /enrollments/           # Crear matriculación
PUT    /enrollments/{id}       # Actualizar matriculación
DELETE /enrollments/{id}       # Eliminar matriculación
```

### **🔄 Sincronización BigQuery**
```http
POST   /sync/bigquery          # Sincronizar todo: Cloud SQL → BigQuery
GET    /sync/status            # Verificar estado de sincronización
```

### **🤖 IA Success Predictor**
```http
GET    /ai/predict-success/{student_identifier}

**Parámetros:**
- `student_identifier`: ID (12), email (erasmo@...), nombre ("Erasmo")
- `include_recommendations`: true/false
- `max_recommendations`: 5
```

## 🌐 **URLs de Producción**

- **🚀 API Base**: https://smartlogix-api-250805843264.us-central1.run.app/
- **📖 Documentación**: https://smartlogix-api-250805843264.us-central1.run.app/docs
- **🔍 Redoc**: https://smartlogix-api-250805843264.us-central1.run.app/redoc
- **📊 Dashboard**: Looker Studio conectado a BigQuery

## 🛠️ **Instalación y Despliegue**

### **Requisitos**
- Python 3.11+
- Google Cloud SDK
- Credenciales GCP configuradas

### **🔧 Desarrollo Local**
```bash
# Clonar repositorio
git clone https://github.com/ErasmoMB/smartlogix-api.git
cd smartlogix-api

# Crear entorno virtual
python -m venv env
env\Scripts\activate  # Windows
source env/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
export DATABASE_URL="postgresql://postgres:postgres123@localhost:5432/smartlogix_db"

# Ejecutar API
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### **☁️ Despliegue Cloud Run**
```bash
# Desplegar con configuración completa
gcloud run deploy smartlogix-api \
  --source . \
  --region=us-central1 \
  --allow-unauthenticated \
  --add-cloudsql-instances=clever-gadget-471116-m6:us-central1:smartlogix-db \
  --set-env-vars="DATABASE_URL=postgresql://postgres:postgres123@/smartlogix_db?host=/cloudsql/clever-gadget-471116-m6:us-central1:smartlogix-db"
```

## 📊 **Datos del Sistema**

### **📈 Estadísticas Actuales**
- **👥 Estudiantes**: 32 registros activos
- **📚 Cursos**: 11 cursos tecnológicos
- **📝 Matriculaciones**: 61 registros con datos reales
- **🏗️ Infraestructura**: 100% Google Cloud Platform
- **🔄 Sincronización**: Tiempo real con BigQuery

### **🗄️ Estructura de Base de Datos**
```sql
-- Tabla students (32 registros)
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla courses (11 registros)  
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla enrollments (61 registros)
CREATE TABLE enrollments (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id),
    course_id INTEGER REFERENCES courses(id),
    estado VARCHAR(20) CHECK (estado IN ('Cursando', 'Aprobado', 'Desaprobado', 'Retirado')),
    puntaje INTEGER CHECK (puntaje >= 0 AND puntaje <= 20),
    fecha_matricula TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🤖 **IA Academic Success Predictor**

### **🧠 Funcionalidades de IA**
- **Análisis de rendimiento**: Promedio, tasa de aprobación, tendencias
- **Predicción de éxito**: Probabilidades específicas por curso
- **Recomendaciones inteligentes**: Basadas en historial académico real
- **Evaluación de riesgo**: Detección temprana de estudiantes en riesgo
- **Búsqueda flexible**: Por ID, email o nombre parcial

### **📊 Ejemplo de Respuesta IA**
```json
{
  "🤖 smartlogix_ai": "Academic Success Predictor v1.0",
  "student_info": {
    "id": 12,
    "nombre": "Erasmo Montufar",
    "email": "montufar@gmail.com"
  },
  "academic_analysis": {
    "promedio_actual": 20.0,
    "cursos_completados": 5,
    "tasa_aprobacion": "100%",
    "tendencia_aprendizaje": "Estable"
  },
  "ai_recommendations": [
    {
      "course_id": 10,
      "titulo": "Blockchain y Criptomonedas",
      "success_probability": "92.1%",
      "predicted_score": "20/20",
      "confidence": "94%"
    }
  ],
  "cloud_processing": {
    "platform": "Google Cloud AI Platform",
    "processing_time": "127ms",
    "confidence_level": "94%"
  }
}
```

## 🔄 **Pipeline de Sincronización**

### **⚡ Proceso Automatizado**
1. **API** recibe datos vía endpoints REST
2. **Cloud SQL** almacena en PostgreSQL 14
3. **Endpoint /sync/bigquery** transfiere datos
4. **BigQuery** procesa para analytics
5. **Looker Studio** visualiza en tiempo real
6. **IA** consume datos para predicciones

### **📋 Comandos de Sincronización**
```bash
# Verificar estado
curl https://smartlogix-api-250805843264.us-central1.run.app/sync/status

# Sincronizar todo
curl -X POST https://smartlogix-api-250805843264.us-central1.run.app/sync/bigquery

# Probar IA
curl https://smartlogix-api-250805843264.us-central1.run.app/ai/predict-success/12
```

## 🏆 **Logros Técnicos**

✅ **API REST** completamente funcional con 21 endpoints  
✅ **Base de datos** con 104 registros totales (32+11+61)  
✅ **Sincronización** automática Cloud SQL ↔ BigQuery  
✅ **IA predictiva** consumiendo datos reales del backend  
✅ **Dashboard** con visualizaciones en tiempo real  
✅ **Sistema educativo** (0-20) implementado  
✅ **Arquitectura cloud-native** 100% Google Cloud  
✅ **Pipeline completo** desde transaccional hasta analítico  

---

## 👨‍💻 **Desarrollador**

**Erasmo Montufar**  
*Tecnologías Emergentes - SmartLogix Academy*

**Proyecto**: Sistema completo de gestión académica con IA predictiva  
**Stack**: FastAPI + Cloud SQL + BigQuery + AI/ML + Looker Studio  
**Infraestructura**: Google Cloud Platform (Cloud Run, Cloud SQL, BigQuery)
