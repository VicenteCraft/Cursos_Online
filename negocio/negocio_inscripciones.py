from datetime import datetime

from peewee import IntegrityError

from auxiliares.validaciones import entero_positivo, validar_progreso
from datos.modelos.curso import Curso
from datos.modelos.inscripcion import Inscripcion
from datos.modelos.persona import Estudiante
from datos.repositorio.repositorio_cursos import curso_por_id
from datos.repositorio.repositorio_inscripciones import (
    cupos_ocupados, guardar_inscripcion, inscripcion_existente, inscripcion_por_id,
)
from datos.repositorio.repositorio_personas import persona_por_id


def inscribir_estudiante(estudiante_id, curso_id):
    estudiante_id = entero_positivo(estudiante_id, 'ID de estudiante')
    curso_id = entero_positivo(curso_id, 'ID de curso')
    # La actualización del curso serializa la comprobación de cupos dentro de la transacción.
    with Inscripcion._meta.database.atomic():
        Curso.update(cupos=Curso.cupos).where(Curso.id == curso_id).execute()
        estudiante = persona_por_id(Estudiante, estudiante_id)
        curso = curso_por_id(curso_id)
        if estudiante is None or not estudiante.habilitado:
            raise ValueError('El estudiante no existe o está deshabilitado.')
        if curso is None or not curso.habilitado or not curso.instructor.habilitado:
            raise ValueError('El curso o su instructor no están habilitados.')
        existente = inscripcion_existente(estudiante_id, curso_id)
        if existente and existente.estado != 'Cancelada':
            raise ValueError('El estudiante ya está inscrito en ese curso.')
        if cupos_ocupados(curso_id) >= curso.cupos:
            raise ValueError('El curso no tiene cupos disponibles.')
        if existente:
            existente.estado = 'Activa'
            existente.progreso = 0
            existente.fecha_inscripcion = datetime.now()
            return guardar_inscripcion(existente)
        try:
            return Inscripcion.create(estudiante=estudiante, curso=curso)
        except IntegrityError:
            raise ValueError('El estudiante ya está inscrito en ese curso.') from None


def actualizar_progreso(identificador, progreso):
    inscripcion = inscripcion_por_id(identificador)
    if inscripcion is None:
        raise ValueError('No existe una inscripción con ese ID.')
    if inscripcion.estado == 'Cancelada':
        raise ValueError('No puedes modificar una inscripción cancelada.')
    nuevo_progreso = validar_progreso(progreso)
    if nuevo_progreso < inscripcion.progreso:
        raise ValueError('El progreso no puede disminuir.')
    inscripcion.progreso = nuevo_progreso
    inscripcion.estado = 'Completada' if inscripcion.progreso == 100 else 'Activa'
    return guardar_inscripcion(inscripcion)


def cancelar_inscripcion(identificador):
    inscripcion = inscripcion_por_id(identificador)
    if inscripcion is None:
        raise ValueError('No existe una inscripción con ese ID.')
    if inscripcion.estado == 'Completada':
        raise ValueError('Una inscripción completada se conserva como historial.')
    if inscripcion.estado == 'Cancelada':
        raise ValueError('La inscripción ya está cancelada.')
    inscripcion.estado = 'Cancelada'
    return guardar_inscripcion(inscripcion)
