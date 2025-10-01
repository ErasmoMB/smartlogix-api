-- Scripts SQL para Cloud SQL (PostgreSQL)
-- SmartLogix Database Schema - Formato exacto del parcial

-- Tabla de estudiantes (formato exacto del parcial)
CREATE TABLE students (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  correo VARCHAR(150) UNIQUE NOT NULL,
  fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de cursos (formato exacto del parcial)
CREATE TABLE courses (
  id SERIAL PRIMARY KEY,
  titulo VARCHAR(150) NOT NULL,
  descripcion TEXT,
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de matrículas (formato exacto del parcial)
CREATE TABLE enrollments (
  id SERIAL PRIMARY KEY,
  student_id INT REFERENCES students(id),
  course_id INT REFERENCES courses(id),
  estado VARCHAR(20) DEFAULT 'Activo',
  puntaje INT DEFAULT 100,
  fecha_matricula TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para mejorar rendimiento
CREATE INDEX idx_students_correo ON students(correo);
CREATE INDEX idx_enrollments_student_id ON enrollments(student_id);
CREATE INDEX idx_enrollments_course_id ON enrollments(course_id);
CREATE INDEX idx_enrollments_estado ON enrollments(estado);

-- Datos de ejemplo para pruebas
INSERT INTO students (nombre, correo) VALUES 
('Juan Pérez', 'juan.perez@email.com'),
('María García', 'maria.garcia@email.com'),
('Carlos López', 'carlos.lopez@email.com'),
('Ana Martínez', 'ana.martinez@email.com'),
('Luis Rodríguez', 'luis.rodriguez@email.com');

INSERT INTO courses (titulo, descripcion) VALUES 
('Introducción a Python', 'Curso básico de programación en Python'),
('JavaScript Avanzado', 'Conceptos avanzados de JavaScript y frameworks'),
('Bases de Datos', 'Diseño y gestión de bases de datos relacionales'),
('Machine Learning', 'Introducción al aprendizaje automático'),
('Cloud Computing', 'Servicios en la nube con Google Cloud Platform');

INSERT INTO enrollments (student_id, course_id, estado, puntaje) VALUES 
(1, 1, 'Activo', 100),
(1, 2, 'Activo', 95),
(2, 1, 'Activo', 88),
(2, 3, 'Inactivo', 75),
(3, 2, 'Activo', 92),
(3, 4, 'Activo', 100),
(4, 1, 'Activo', 85),
(4, 5, 'Inactivo', 60),
(5, 3, 'Activo', 98),
(5, 4, 'Activo', 100);

INSERT INTO courses (titulo, descripcion) VALUES 
    ('Introducción a Python', 'Curso básico de programación en Python para principiantes'),
    ('Desarrollo Web con FastAPI', 'Aprende a crear APIs REST modernas con FastAPI'),
    ('Base de Datos con PostgreSQL', 'Fundamentos de bases de datos relacionales'),
    ('Cloud Computing con GCP', 'Introducción a Google Cloud Platform');

INSERT INTO enrollments (student_id, course_id, estado, puntaje) VALUES 
    (1, 1, 'Activo', 100),
    (1, 2, 'Activo', 85),
    (2, 1, 'Activo', 92),
    (2, 3, 'Inactivo', 75),
    (3, 2, 'Activo', 88),
    (4, 1, 'Activo', 95),
    (4, 4, 'Activo', 100);