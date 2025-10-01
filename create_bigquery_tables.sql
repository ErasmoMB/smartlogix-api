-- Crear tabla students en BigQuery
CREATE TABLE `clever-gadget-471116-m6.academy_dataset.students` (
  id INT64,
  nombre STRING,
  correo STRING,
  fecha_registro TIMESTAMP
);

-- Crear tabla courses en BigQuery  
CREATE TABLE `clever-gadget-471116-m6.academy_dataset.courses` (
  id INT64,
  titulo STRING,
  descripcion STRING,
  fecha_creacion TIMESTAMP
);

-- Crear tabla enrollments en BigQuery
CREATE TABLE `clever-gadget-471116-m6.academy_dataset.enrollments` (
  id INT64,
  student_id INT64,
  course_id INT64,
  estado STRING,
  puntaje INT64,
  fecha_matricula TIMESTAMP
);