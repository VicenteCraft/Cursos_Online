from datos.modelos.persona import Estudiante
from datos.repositorio.repositorio_inscripciones import listado_inscripciones
from negocio.negocio_inscripciones import (
    actualizar_progreso, cancelar_inscripcion, inscribir_estudiante,
)
from presentacion.presentacion_cursos import mostrar_cursos
from presentacion.presentacion_personas import mostrar_personas
from presentacion.utilidades import mostrar_tabla, pedir_id, submenu


def mostrar_inscripciones(estudiante_id=None):
    inscripciones = listado_inscripciones()
    if estudiante_id is not None:
        inscripciones = inscripciones.where(inscripciones.model.estudiante == estudiante_id)
    mostrar_tabla(
        ['ID', 'Estudiante', 'Curso', 'Fecha', 'Progreso', 'Estado'],
        ([inscripcion.id, inscripcion.estudiante.nombre, inscripcion.curso.titulo,
          inscripcion.fecha_inscripcion.strftime('%d/%m/%Y'),
          f'{inscripcion.progreso}%', inscripcion.estado] for inscripcion in inscripciones),
    )


def presentar_inscripcion():
    mostrar_personas(Estudiante)
    estudiante_id = pedir_id('ID del estudiante: ')
    mostrar_cursos()
    curso_id = pedir_id('ID del curso: ')
    inscripcion = inscribir_estudiante(estudiante_id, curso_id)
    print(f'Inscripción registrada con ID {inscripcion.id}.')


def presentar_progreso():
    mostrar_inscripciones()
    identificador = pedir_id('ID de la inscripción: ')
    inscripcion = actualizar_progreso(identificador, input('Progreso (0-100): '))
    print(f'Progreso actualizado: {inscripcion.progreso}% - {inscripcion.estado}.')


def presentar_cancelacion():
    mostrar_inscripciones()
    identificador = pedir_id('ID de la inscripción: ')
    if input('¿Confirmar cancelación? [s/N]: ').strip().lower() == 's':
        cancelar_inscripcion(identificador)
        print('Inscripción cancelada. Se ha liberado el cupo.')


def menu_inscripciones():
    submenu('Inscripciones', {
        '1': ('Listar inscripciones', mostrar_inscripciones),
        '2': ('Inscribir estudiante en un curso', presentar_inscripcion),
        '3': ('Actualizar progreso', presentar_progreso),
        '4': ('Cancelar inscripción', presentar_cancelacion),
        '5': ('Consultar por estudiante', lambda: mostrar_inscripciones(pedir_id('ID de estudiante: '))),
    })
