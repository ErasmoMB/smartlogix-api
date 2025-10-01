-- Consultas SQL para BigQuery - SmartLogix Academic Dataset
-- Dataset: academy_dataset

-- ============================================
-- QUERY PRINCIPAL DEL PARCIAL (EXACTO)
-- ============================================
-- El total de estudiantes activos por curso
-- El promedio de puntaje por curso
SELECT 
  c.titulo,
  COUNTIF(e.estado = 'Activo') AS total_activos,
  AVG(e.puntaje) AS promedio_puntaje
FROM `academy_dataset.enrollments` e
JOIN `academy_dataset.courses` c ON e.course_id = c.id
GROUP BY c.titulo;

-- ============================================
-- QUERIES ADICIONALES PARA EL DASHBOARD
-- ============================================

-- 1. Resumen general del sistema
SELECT 
  COUNT(DISTINCT s.id) as total_estudiantes,
  COUNT(DISTINCT c.id) as total_cursos,
  COUNT(e.id) as total_matriculas,
  COUNTIF(e.estado = 'Activo') as matriculas_activas,
  COUNTIF(e.estado = 'Inactivo') as matriculas_inactivas,
  ROUND(AVG(e.puntaje), 2) as puntaje_promedio_general
FROM `academy_dataset.students` s
CROSS JOIN `academy_dataset.courses` c
LEFT JOIN `academy_dataset.enrollments` e ON s.id = e.student_id OR c.id = e.course_id;

-- 2. Detalle por curso (para gráfico de barras)
SELECT 
  c.titulo as curso,
  c.descripcion,
  COUNT(e.id) as total_matriculas,
  COUNTIF(e.estado = 'Activo') as estudiantes_activos,
  COUNTIF(e.estado = 'Inactivo') as estudiantes_inactivos,
  ROUND(AVG(e.puntaje), 2) as promedio_puntaje
FROM `academy_dataset.courses` c
LEFT JOIN `academy_dataset.enrollments` e ON c.id = e.course_id
GROUP BY c.id, c.titulo, c.descripcion
ORDER BY estudiantes_activos DESC;

-- 3. Top estudiantes (para indicadores)
SELECT 
  s.nombre,
  s.correo,
  COUNT(e.id) as cursos_matriculados,
  COUNTIF(e.estado = 'Activo') as cursos_activos,
  ROUND(AVG(e.puntaje), 2) as puntaje_promedio
FROM `academy_dataset.students` s
LEFT JOIN `academy_dataset.enrollments` e ON s.id = e.student_id
GROUP BY s.id, s.nombre, s.correo
HAVING COUNT(e.id) > 0
ORDER BY puntaje_promedio DESC
LIMIT 10;

-- 4. Análisis temporal de matrículas
SELECT 
  EXTRACT(YEAR FROM e.fecha_matricula) as año,
  EXTRACT(MONTH FROM e.fecha_matricula) as mes,
  COUNT(*) as nuevas_matriculas,
  COUNTIF(e.estado = 'Activo') as matriculas_activas,
  ROUND(AVG(e.puntaje), 2) as puntaje_promedio_inicial
FROM `academy_dataset.enrollments` e
GROUP BY año, mes
ORDER BY año DESC, mes DESC;

-- 5. Tasa de retención por curso
SELECT 
  c.titulo,
  COUNT(e.id) as total_matriculas,
  COUNTIF(e.estado = 'Activo') as estudiantes_activos,
  COUNTIF(e.estado = 'Inactivo') as estudiantes_retirados,
  ROUND(COUNTIF(e.estado = 'Activo') * 100.0 / COUNT(e.id), 2) as tasa_retencion_pct,
  ROUND(COUNTIF(e.estado = 'Inactivo') * 100.0 / COUNT(e.id), 2) as tasa_desercion_pct
FROM `academy_dataset.courses` c
LEFT JOIN `academy_dataset.enrollments` e ON c.id = e.course_id
GROUP BY c.id, c.titulo
HAVING COUNT(e.id) > 0
ORDER BY tasa_retencion_pct DESC;