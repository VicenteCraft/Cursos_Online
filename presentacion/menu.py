from datos import nombre_app, version_app
from datos.modelos import Curso, Estudiante, Inscripcion, Instructor
from presentacion.presentacion_cursos import menu_cursos
from presentacion.presentacion_inscripciones import menu_inscripciones
from presentacion.presentacion_personas import menu_personas
from presentacion.presentacion_usuarios import presentar_cambio_contrasenia
from presentacion.utilidades import ejecutar_accion, mostrar_tabla


def mostrar_resumen():
    mostrar_tabla(['Indicador', 'Total'], [
        ['Estudiantes habilitados', Estudiante.select().where(Estudiante.habilitado == True).count()],
        ['Instructores habilitados', Instructor.select().where(Instructor.habilitado == True).count()],
        ['Cursos habilitados', Curso.select().where(Curso.habilitado == True).count()],
        ['Inscripciones activas', Inscripcion.select().where(Inscripcion.estado == 'Activa').count()],
        ['Cursos completados', Inscripcion.select().where(Inscripcion.estado == 'Completada').count()],
        ['Inscripciones canceladas', Inscripcion.select().where(Inscripcion.estado == 'Cancelada').count()],
    ])


def menu_principal(usuario):
    acciones = {
        '1': ('Gestionar cursos', menu_cursos),
        '2': ('Gestionar estudiantes', lambda: menu_personas(Estudiante)),
        '3': ('Gestionar instructores', lambda: menu_personas(Instructor)),
        '4': ('Gestionar inscripciones y progreso', menu_inscripciones),
        '5': ('Ver resumen de la academia', mostrar_resumen),
        '6': ('Cambiar contraseña', lambda: presentar_cambio_contrasenia(usuario)),
    }
    while True:
        print(f'\n=== {nombre_app} {version_app} ===')
        for clave, (etiqueta, _) in acciones.items():
            print(f'[{clave}] {etiqueta}')
        print('[0] Salir')
        opcion = input('Seleccione una opción: ').strip()
        if opcion == '0':
            print('Gracias por utilizar Academia Online.')
            return
        if opcion in acciones:
            ejecutar_accion(acciones[opcion][1])
        else:
            print('Opción no válida.')
