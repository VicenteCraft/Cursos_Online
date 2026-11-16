-- Academia Online: datos de ejemplo ficticios.
-- Compatible con SQLite y MySQL. En MySQL, selecciona primero la base de datos.
-- Ejecutar después de iniciar main.py al menos una vez para crear las tablas.
-- Los precios están expresados en pesos chilenos (CLP).
-- No se fijan IDs: las relaciones se resuelven mediante correos y títulos únicos.
-- Puede repetirse: los registros existentes se conservan sin modificarlos.
-- El administrador y su contraseña se crean desde la aplicación, no desde este SQL.

BEGIN;

-- 1. Instructores
INSERT INTO instructores (nombre, correo, especialidad, habilitado, fecha_registro)
SELECT nuevos.nombre, nuevos.correo, nuevos.especialidad, 1, CURRENT_TIMESTAMP
FROM (
    SELECT 'Diego Muñoz' AS nombre, 'diego.munoz@example.com' AS correo,
           'Programación orientada a objetos' AS especialidad
    UNION ALL
    SELECT 'Valentina Rojas', 'valentina.rojas@example.com', 'Diseño y desarrollo web'
    UNION ALL
    SELECT 'Felipe Torres', 'felipe.torres@example.com', 'Bases de datos y análisis de datos'
) AS nuevos
WHERE NOT EXISTS (
    SELECT 1 FROM instructores WHERE instructores.correo = nuevos.correo
);

-- 2. Estudiantes
INSERT INTO estudiantes (nombre, correo, habilitado, fecha_registro)
SELECT nuevos.nombre, nuevos.correo, 1, CURRENT_TIMESTAMP
FROM (
    SELECT 'Sofía González' AS nombre, 'sofia.gonzalez@example.com' AS correo
    UNION ALL
    SELECT 'Benjamín Pérez', 'benjamin.perez@example.com'
    UNION ALL
    SELECT 'Isidora Silva', 'isidora.silva@example.com'
    UNION ALL
    SELECT 'Matías Fernández', 'matias.fernandez@example.com'
    UNION ALL
    SELECT 'Antonia Díaz', 'antonia.diaz@example.com'
    UNION ALL
    SELECT 'Vicente Herrera', 'vicente.herrera@example.com'
) AS nuevos
WHERE NOT EXISTS (
    SELECT 1 FROM estudiantes WHERE estudiantes.correo = nuevos.correo
);

-- 3. Cursos: el instructor se obtiene por su correo.
INSERT INTO cursos
    (titulo, descripcion, instructor_id, duracion_horas, precio, cupos, habilitado)
SELECT nuevos.titulo, nuevos.descripcion, instructores.id,
       nuevos.duracion_horas, nuevos.precio, nuevos.cupos, 1
FROM (
    SELECT 'Programación orientada a objetos con Python' AS titulo,
           'Clases, objetos, herencia y polimorfismo mediante ejercicios prácticos.' AS descripcion,
           'diego.munoz@example.com' AS correo_instructor,
           40 AS duracion_horas, 44990.00 AS precio, 20 AS cupos
    UNION ALL
    SELECT 'Diseño web con HTML y CSS',
           'Construcción de sitios web adaptables a distintos dispositivos.',
           'valentina.rojas@example.com', 30, 29990.00, 25
    UNION ALL
    SELECT 'Bases de datos con SQL',
           'Diseño relacional, consultas SQL y relaciones entre tablas.',
           'felipe.torres@example.com', 35, 34990.00, 20
    UNION ALL
    SELECT 'Introducción al análisis de datos',
           'Primeros pasos para organizar, explorar e interpretar conjuntos de datos.',
           'felipe.torres@example.com', 15, 0.00, 30
) AS nuevos
JOIN instructores ON instructores.correo = nuevos.correo_instructor
WHERE NOT EXISTS (
    SELECT 1 FROM cursos WHERE cursos.titulo = nuevos.titulo
);

-- 4. Inscripciones: un estudiante puede participar en varios cursos.
-- Activa: progreso de 0 a 99. Completada: 100. Cancelada: no ocupa cupo.
INSERT INTO inscripciones
    (estudiante_id, curso_id, fecha_inscripcion, progreso, estado)
SELECT estudiantes.id, cursos.id, CURRENT_TIMESTAMP, nuevos.progreso, nuevos.estado
FROM (
    SELECT 'sofia.gonzalez@example.com' AS correo_estudiante,
           'Programación orientada a objetos con Python' AS titulo_curso,
           50 AS progreso, 'Activa' AS estado
    UNION ALL
    SELECT 'benjamin.perez@example.com', 'Programación orientada a objetos con Python', 25, 'Activa'
    UNION ALL
    SELECT 'isidora.silva@example.com', 'Diseño web con HTML y CSS', 100, 'Completada'
    UNION ALL
    SELECT 'matias.fernandez@example.com', 'Bases de datos con SQL', 70, 'Activa'
    UNION ALL
    SELECT 'antonia.diaz@example.com', 'Introducción al análisis de datos', 0, 'Activa'
    UNION ALL
    SELECT 'vicente.herrera@example.com', 'Bases de datos con SQL', 100, 'Completada'
    UNION ALL
    SELECT 'sofia.gonzalez@example.com', 'Introducción al análisis de datos', 10, 'Activa'
    UNION ALL
    SELECT 'benjamin.perez@example.com', 'Diseño web con HTML y CSS', 20, 'Cancelada'
) AS nuevos
JOIN estudiantes ON estudiantes.correo = nuevos.correo_estudiante
JOIN cursos ON cursos.titulo = nuevos.titulo_curso
WHERE NOT EXISTS (
    SELECT 1 FROM inscripciones
    WHERE inscripciones.estudiante_id = estudiantes.id
      AND inscripciones.curso_id = cursos.id
)
AND estudiantes.habilitado = 1
AND cursos.habilitado = 1
AND EXISTS (
    SELECT 1 FROM instructores
    WHERE instructores.id = cursos.instructor_id AND instructores.habilitado = 1
)
-- Reserva margen para todas las inscripciones de este lote si el curso ya tiene datos.
AND (
    nuevos.estado = 'Cancelada'
    OR cursos.cupos >= (
        SELECT COUNT(*) FROM inscripciones
        WHERE inscripciones.curso_id = cursos.id AND inscripciones.estado <> 'Cancelada'
    ) + CASE
        WHEN cursos.titulo IN (
            'Programación orientada a objetos con Python', 'Bases de datos con SQL',
            'Introducción al análisis de datos'
        ) THEN 2
        ELSE 1
    END
);

COMMIT;
