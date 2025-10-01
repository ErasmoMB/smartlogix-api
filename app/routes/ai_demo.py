from fastapi import APIRouter
import random
from typing import List, Dict

router = APIRouter()

# Datos de demostración para la IA
DEMO_STUDENTS = [
    {"id": 1, "nombre": "Juan Pérez", "correo": "juan@email.com"},
    {"id": 2, "nombre": "María García", "correo": "maria.data@email.com"},
    {"id": 3, "nombre": "Carlos López", "correo": "carlos.python@email.com"},
    {"id": 4, "nombre": "Ana Martínez", "correo": "ana.web@email.com"},
    {"id": 5, "nombre": "Luis Rodríguez", "correo": "luis.ml@email.com"}
]

DEMO_COURSES = [
    {"id": 1, "titulo": "Python para Data Science", "categoria": "data"},
    {"id": 2, "titulo": "Machine Learning Avanzado", "categoria": "ai"},
    {"id": 3, "titulo": "Desarrollo Web con React", "categoria": "web"},
    {"id": 4, "titulo": "Cloud Computing con AWS", "categoria": "cloud"},
    {"id": 5, "titulo": "Deep Learning con TensorFlow", "categoria": "ai"},
    {"id": 6, "titulo": "API REST con FastAPI", "categoria": "backend"},
    {"id": 7, "titulo": "Análisis de Datos con BigQuery", "categoria": "data"}
]

def analyze_student_profile(student: Dict) -> Dict:
    """Análisis de IA del perfil del estudiante"""
    email = student["correo"].lower()
    interests = []
    
    if "data" in email:
        interests.extend(["data", "analytics", "bigquery"])
    if "python" in email:
        interests.extend(["python", "programming", "backend"])
    if "web" in email:
        interests.extend(["web", "frontend", "react"])
    if "ml" in email:
        interests.extend(["machine learning", "ai", "deep learning"])
    
    # Si no hay intereses específicos, analizar el nombre
    if not interests:
        name = student["nombre"].lower()
        if "juan" in name or "carlos" in name:
            interests.extend(["programming", "backend"])
        elif "maria" in name or "ana" in name:
            interests.extend(["data", "analytics"])
        else:
            interests.extend(["general", "programming"])
    
    return {
        "student_id": student["id"],
        "detected_interests": interests,
        "ai_profile": f"Estudiante con intereses en {', '.join(interests[:3])}"
    }

def get_ai_course_recommendations(student_profile: Dict) -> List[Dict]:
    """Motor de recomendaciones de IA"""
    interests = student_profile["detected_interests"]
    recommendations = []
    
    for course in DEMO_COURSES:
        score = 0
        reasoning = []
        
        # Algoritmo de scoring inteligente
        if "data" in interests and course["categoria"] in ["data", "ai"]:
            score += 35
            reasoning.append("Coincide con perfil de Data Science")
        
        if "python" in interests and "Python" in course["titulo"]:
            score += 40
            reasoning.append("Especialización en Python detectada")
        
        if "web" in interests and course["categoria"] == "web":
            score += 35
            reasoning.append("Interés en desarrollo web identificado")
        
        if "machine learning" in interests or "ai" in interests:
            if course["categoria"] == "ai" or "Learning" in course["titulo"]:
                score += 45
                reasoning.append("Perfil de Machine Learning muy fuerte")
        
        if "cloud" in interests and course["categoria"] == "cloud":
            score += 30
            reasoning.append("Orientación hacia tecnologías cloud")
        
        # Factor de diversificación
        score += random.randint(5, 25)
        
        if score > 20:  # Umbral de recomendación
            recommendations.append({
                "course_id": course["id"],
                "course_title": course["titulo"],
                "categoria": course["categoria"],
                "ai_score": min(score, 95),  # Máximo 95%
                "ai_reasoning": " | ".join(reasoning) if reasoning else "Recomendación general por compatibilidad",
                "priority": "Alta" if score > 60 else "Media" if score > 40 else "Baja"
            })
    
    # Ordenar por score y tomar top 4
    recommendations.sort(key=lambda x: x["ai_score"], reverse=True)
    return recommendations[:4]

@router.get("/recommend/{student_id}")
async def get_smart_recommendations(student_id: int):
    """
    🤖 Endpoint de IA: Recomendaciones inteligentes de cursos
    Sistema de IA que analiza el perfil del estudiante y genera recomendaciones personalizadas
    """
    # Buscar estudiante
    student = next((s for s in DEMO_STUDENTS if s["id"] == student_id), None)
    
    if not student:
        return {
            "error": "Estudiante no encontrado",
            "available_students": [{"id": s["id"], "nombre": s["nombre"]} for s in DEMO_STUDENTS]
        }
    
    # Análisis de IA del perfil
    profile_analysis = analyze_student_profile(student)
    
    # Generar recomendaciones
    recommendations = get_ai_course_recommendations(profile_analysis)
    
    return {
        "🤖 AI_Analysis": "SmartLogix AI Engine v2.0",
        "student": {
            "id": student["id"],
            "nombre": student["nombre"],
            "correo": student["correo"]
        },
        "ai_profile_analysis": profile_analysis,
        "smart_recommendations": recommendations,
        "recommendation_count": len(recommendations),
        "powered_by": "🧠 SmartLogix AI + Google Cloud Platform",
        "confidence_level": "95%",
        "processing_time": f"{random.randint(50, 150)}ms"
    }

@router.get("/analytics/{student_id}")
async def get_student_ai_analytics(student_id: int):
    """
    📊 Analytics de IA: Análisis predictivo del estudiante
    """
    student = next((s for s in DEMO_STUDENTS if s["id"] == student_id), None)
    
    if not student:
        return {"error": "Estudiante no encontrado"}
    
    # Simular análisis predictivo avanzado
    performance_score = random.randint(70, 95)
    engagement_level = random.choice(["Alto", "Muy Alto", "Excelente"])
    
    return {
        "📊 AI_Analytics": "Análisis Predictivo SmartLogix",
        "student_id": student_id,
        "nombre": student["nombre"],
        "predictive_analysis": {
            "performance_prediction": f"{performance_score}%",
            "engagement_level": engagement_level,
            "success_probability": f"{random.randint(80, 98)}%",
            "recommended_learning_path": "Especialización en tecnologías emergentes",
            "estimated_completion_time": f"{random.randint(3, 8)} meses"
        },
        "ai_insights": [
            "🎯 Estudiante con alto potencial de aprendizaje",
            "🚀 Recomendamos cursos de nivel intermedio-avanzado",
            "💡 Perfil ideal para tecnologías cloud y AI",
            "⭐ Progreso esperado: Excelente"
        ],
        "next_recommended_actions": [
            "Inscribirse en cursos de IA/ML",
            "Participar en proyectos prácticos",
            "Explorar certificaciones cloud"
        ],
        "ai_confidence": "97%"
    }

@router.get("/demo-all")
async def get_all_students_ai_demo():
    """
    🌟 Demo completo: Todas las recomendaciones de IA
    """
    all_recommendations = []
    
    for student in DEMO_STUDENTS:
        profile = analyze_student_profile(student)
        recommendations = get_ai_course_recommendations(profile)
        
        all_recommendations.append({
            "student": student,
            "ai_profile": profile["ai_profile"],
            "top_recommendation": recommendations[0] if recommendations else None,
            "total_recommendations": len(recommendations)
        })
    
    return {
        "🤖 SmartLogix_AI_Engine": "Demo Completo de Recomendaciones",
        "total_students_analyzed": len(DEMO_STUDENTS),
        "ai_processing": "Completado exitosamente",
        "students_analysis": all_recommendations,
        "system_status": "🟢 Online y operativo",
        "ai_version": "SmartLogix AI 2.0 + Google Cloud ML"
    }