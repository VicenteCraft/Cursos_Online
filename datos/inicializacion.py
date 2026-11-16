from auxiliares.seguridad import generar_hash
from datos.conexion import database
from datos.modelos import MODELOS, Curso, Instructor, Usuario


def inicializar_datos():
    database.create_tables(MODELOS)
    with database.atomic():
        # Los ejemplos se cargan solo al crear el primer usuario del sistema.
        if Usuario.select().exists():
            return
        Usuario.create(nombre='admin', password_hash=generar_hash('Admin123!'))
        instructor = Instructor.create(
            nombre='Camila Soto', correo='camila@academia.example',
            especialidad='Programación y desarrollo web',
        )
        Curso.create(
            titulo='Python desde cero', descripcion='Fundamentos y ejercicios de programación.',
            instructor=instructor, duracion_horas=30, precio=29990, cupos=25,
        )
        Curso.create(
            titulo='Desarrollo web inicial', descripcion='Introducción a HTML, CSS y JavaScript.',
            instructor=instructor, duracion_horas=40, precio=39990, cupos=20,
        )
