import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from peewee import SqliteDatabase

from datos.modelos import MODELOS, Curso, Estudiante, Inscripcion, Instructor, Usuario
from negocio.negocio_cursos import guardar_datos_curso
from negocio.negocio_inscripciones import (
    actualizar_progreso, cancelar_inscripcion, inscribir_estudiante,
)
from negocio.negocio_personas import cambiar_estado_persona, guardar_datos_persona
from negocio.negocio_usuarios import autenticar_usuario, cambiar_contrasenia, crear_usuario
from presentacion.menu import menu_principal
from presentacion.presentacion_cursos import mostrar_cursos
from presentacion.presentacion_inscripciones import mostrar_inscripciones


class AcademiaTest(unittest.TestCase):
    def setUp(self):
        self.db = SqliteDatabase(':memory:', pragmas={'foreign_keys': 1})
        self.contexto = self.db.bind_ctx(MODELOS)
        self.contexto.__enter__()
        self.db.connect()
        self.db.create_tables(MODELOS)
        self.instructor = guardar_datos_persona(
            Instructor, 'Ana Docente', 'ana@example.com', 'Python',
        )
        self.estudiante = guardar_datos_persona(Estudiante, 'Luis Pérez', 'luis@example.com')
        self.curso = guardar_datos_curso('Python', 'Curso inicial', self.instructor.id, 20, 9900, 1)

    def tearDown(self):
        self.db.close()
        self.contexto.__exit__(None, None, None)

    def test_autenticacion_y_cambio_contrasenia(self):
        usuario = crear_usuario('admin', 'Admin123!')
        self.assertIsNone(autenticar_usuario('admin', 'incorrecta'))
        self.assertIsNone(autenticar_usuario('desconocido', 'Admin123!'))
        self.assertEqual(autenticar_usuario('admin', 'Admin123!').id, usuario.id)
        self.assertNotEqual(usuario.password_hash, 'Admin123!')
        cambiar_contrasenia(usuario, 'Admin123!', 'OtraClave123!')
        self.assertIsNone(autenticar_usuario('admin', 'Admin123!'))
        self.assertIsNotNone(autenticar_usuario('admin', 'OtraClave123!'))

    def test_cupo_duplicado_cancelacion_y_reinscripcion(self):
        inscripcion = inscribir_estudiante(self.estudiante.id, self.curso.id)
        with self.assertRaisesRegex(ValueError, 'ya está inscrito'):
            inscribir_estudiante(self.estudiante.id, self.curso.id)
        otro = guardar_datos_persona(Estudiante, 'María', 'maria@example.com')
        with self.assertRaisesRegex(ValueError, 'cupos disponibles'):
            inscribir_estudiante(otro.id, self.curso.id)
        actualizar_progreso(inscripcion.id, 50)
        cancelar_inscripcion(inscripcion.id)
        otra = inscribir_estudiante(otro.id, self.curso.id)
        cancelar_inscripcion(otra.id)
        reinscripcion = inscribir_estudiante(self.estudiante.id, self.curso.id)
        self.assertEqual(reinscripcion.id, inscripcion.id)
        self.assertEqual(reinscripcion.progreso, 0)
        self.assertEqual(reinscripcion.estado, 'Activa')
        self.assertEqual(Inscripcion.select().count(), 2)

    def test_progreso_y_finalizacion(self):
        inscripcion = inscribir_estudiante(self.estudiante.id, self.curso.id)
        actualizar_progreso(inscripcion.id, 40)
        for invalido in (-1, 101, 'abc', 20):
            with self.assertRaises(ValueError):
                actualizar_progreso(inscripcion.id, invalido)
        completada = actualizar_progreso(inscripcion.id, 100)
        self.assertEqual(completada.estado, 'Completada')
        with self.assertRaisesRegex(ValueError, 'completada'):
            cancelar_inscripcion(inscripcion.id)

    def test_entidades_deshabilitadas_impiden_inscripcion(self):
        cambiar_estado_persona(Estudiante, self.estudiante.id)
        with self.assertRaisesRegex(ValueError, 'estudiante'):
            inscribir_estudiante(self.estudiante.id, self.curso.id)
        cambiar_estado_persona(Estudiante, self.estudiante.id)
        cambiar_estado_persona(Instructor, self.instructor.id)
        with self.assertRaisesRegex(ValueError, 'instructor'):
            inscribir_estudiante(self.estudiante.id, self.curso.id)
        cambiar_estado_persona(Instructor, self.instructor.id)
        self.curso.habilitado = False
        self.curso.save()
        with self.assertRaisesRegex(ValueError, 'curso'):
            inscribir_estudiante(self.estudiante.id, self.curso.id)

    def test_validaciones_y_edicion_persistente(self):
        for correo in ('sin-arroba', 'luis@example.com'):
            with self.assertRaises(ValueError):
                guardar_datos_persona(Estudiante, 'Otro', correo)
        for precio in ('-1', 'NaN', '1.234'):
            with self.assertRaises(ValueError):
                guardar_datos_curso('Inválido', 'Descripción', self.instructor.id, 10, precio, 5)
        inscribir_estudiante(self.estudiante.id, self.curso.id)
        segundo = guardar_datos_persona(Estudiante, 'Otro', 'otro@example.com')
        guardar_datos_curso('Python avanzado', 'Actualizado', self.instructor.id, 40, 0, 2, self.curso.id)
        inscribir_estudiante(segundo.id, self.curso.id)
        with self.assertRaisesRegex(ValueError, 'inscripciones vigentes'):
            guardar_datos_curso('Python avanzado', 'Actualizado', self.instructor.id, 40, 0, 1, self.curso.id)
        self.assertEqual(Curso.get_by_id(self.curso.id).cupos, 2)
        self.assertEqual(Curso.get_by_id(self.curso.id).titulo, 'Python avanzado')

    def test_presentacion_de_datos_y_menu(self):
        inscribir_estudiante(self.estudiante.id, self.curso.id)
        salida = StringIO()
        with redirect_stdout(salida), patch('builtins.input', side_effect=['5', '1', '1', '0', '0']):
            mostrar_cursos()
            mostrar_inscripciones(self.estudiante.id)
            menu_principal(Usuario(nombre='admin'))
        texto = salida.getvalue()
        self.assertIn('Python', texto)
        self.assertIn('Luis Pérez', texto)
        self.assertIn('Inscripciones activas', texto)
        self.assertIn('Gracias por utilizar', texto)

    def test_inicializacion_es_idempotente(self):
        from datos.inicializacion import inicializar_datos

        with patch('datos.inicializacion.database', self.db):
            inicializar_datos()
            inicializar_datos()
        self.assertEqual(Usuario.select().count(), 1)
        self.assertEqual(Curso.select().count(), 3)
        self.assertIsNotNone(autenticar_usuario('admin', 'Admin123!'))


if __name__ == '__main__':
    unittest.main()
