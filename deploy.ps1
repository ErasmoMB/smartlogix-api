# Script de despliegue para Cloud Run
Write-Host "🚀 Desplegando SmartLogix API en Google Cloud Run..."

# Variables
$PROJECT_ID = "clever-gadget-471116-m6"
$SERVICE_NAME = "smartlogix-api"
$REGION = "us-central1"
$DB_CONNECTION = "clever-gadget-471116-m6:us-central1:smartlogix-db"

# Crear imagen en Container Registry
Write-Host "📦 Construyendo imagen Docker..."
.\gcloud.ps1 builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Desplegar en Cloud Run
Write-Host "🌟 Desplegando en Cloud Run..."
.\gcloud.ps1 run deploy $SERVICE_NAME `
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME `
  --platform managed `
  --region $REGION `
  --allow-unauthenticated `
  --add-cloudsql-instances $DB_CONNECTION `
  --set-env-vars "DB_USER=postgres,DB_PASSWORD=SmartLogix2024!,DB_NAME=smartlogix_db,CLOUD_SQL_CONNECTION_NAME=$DB_CONNECTION,ENVIRONMENT=production" `
  --memory 512Mi `
  --cpu 1 `
  --concurrency 80 `
  --timeout 300

Write-Host "✅ Despliegue completado!"
Write-Host "🌐 Tu API estará disponible en la URL que se muestra arriba"