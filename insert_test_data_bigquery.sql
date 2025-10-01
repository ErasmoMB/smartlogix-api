-- Insertar datos de prueba directamente en BigQuery
-- Para que el dashboard funcione con datos de ejemplo

-- Insertar estudiantes de prueba
INSERT INTO `clever-gadget-471116-m6.academy_dataset.students` VALUES
(1, 'Juan Pérez', 'juan.perez@email.com', CURRENT_TIMESTAMP()),
(2, 'María García', 'maria.garcia@email.com', CURRENT_TIMESTAMP()),
(3, 'Carlos López', 'carlos.lopez@email.com', CURRENT_TIMESTAMP()),
(4, 'Ana Martínez', 'ana.martinez@email.com', CURRENT_TIMESTAMP()),
(5, 'Luis Rodríguez', 'luis.rodriguez@email.com', CURRENT_TIMESTAMP()),
(6, 'Sofia Hernández', 'sofia.hernandez@email.com', CURRENT_TIMESTAMP()),
(7, 'Diego Torres', 'diego.torres@email.com', CURRENT_TIMESTAMP()),
(8, 'Laura Sánchez', 'laura.sanchez@email.com', CURRENT_TIMESTAMP());

-- Insertar cursos de prueba
INSERT INTO `clever-gadget-471116-m6.academy_dataset.courses` VALUES
(1, 'Introducción a Python', 'Curso básico de programación en Python', CURRENT_TIMESTAMP()),
(2, 'JavaScript Avanzado', 'Conceptos avanzados de JavaScript y frameworks', CURRENT_TIMESTAMP()),
(3, 'Bases de Datos', 'Diseño y gestión de bases de datos relacionales', CURRENT_TIMESTAMP()),
(4, 'Machine Learning', 'Introducción al aprendizaje automático', CURRENT_TIMESTAMP()),
(5, 'Cloud Computing', 'Servicios en la nube con Google Cloud Platform', CURRENT_TIMESTAMP());

-- Insertar matrículas de prueba (con estudiantes activos e inactivos)
INSERT INTO `clever-gadget-471116-m6.academy_dataset.enrollments` VALUES
-- Python (curso más popular)
(1, 1, 1, 'Activo', 95, CURRENT_TIMESTAMP()),
(2, 2, 1, 'Activo', 88, CURRENT_TIMESTAMP()),
(3, 4, 1, 'Activo', 92, CURRENT_TIMESTAMP()),
(4, 5, 1, 'Inactivo', 78, CURRENT_TIMESTAMP()),
(5, 8, 1, 'Activo', 89, CURRENT_TIMESTAMP()),

-- JavaScript
(6, 1, 2, 'Activo', 87, CURRENT_TIMESTAMP()),
(7, 3, 2, 'Activo', 91, CURRENT_TIMESTAMP()),
(8, 6, 2, 'Inactivo', 76, CURRENT_TIMESTAMP()),

-- Bases de Datos
(9, 1, 3, 'Activo', 93, CURRENT_TIMESTAMP()),
(10, 4, 3, 'Activo', 85, CURRENT_TIMESTAMP()),
(11, 7, 3, 'Activo', 90, CURRENT_TIMESTAMP()),

-- Machine Learning
(12, 2, 4, 'Activo', 94, CURRENT_TIMESTAMP()),
(13, 4, 4, 'Activo', 87, CURRENT_TIMESTAMP()),
(14, 6, 4, 'Activo', 91, CURRENT_TIMESTAMP()),
(15, 8, 4, 'Inactivo', 72, CURRENT_TIMESTAMP()),

-- Cloud Computing
(16, 3, 5, 'Activo', 88, CURRENT_TIMESTAMP()),
(17, 5, 5, 'Activo', 92, CURRENT_TIMESTAMP()),
(18, 7, 5, 'Activo', 86, CURRENT_TIMESTAMP());

-- Verificar los datos insertados
SELECT 'Estudiantes' as tabla, COUNT(*) as total FROM `clever-gadget-471116-m6.academy_dataset.students`
UNION ALL
SELECT 'Cursos' as tabla, COUNT(*) as total FROM `clever-gadget-471116-m6.academy_dataset.courses`
UNION ALL  
SELECT 'Matrículas' as tabla, COUNT(*) as total FROM `clever-gadget-471116-m6.academy_dataset.enrollments`;