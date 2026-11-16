from datos.modelos.curso import Curso
from datos.modelos.inscripcion import Inscripcion
from datos.modelos.persona import Estudiante


def listado_inscripciones():
    return (Inscripcion.select(Inscripcion, Estudiante, Curso)
            .join(Estudiante).switch(Inscripcion).join(Curso)
            .order_by(Inscripcion.id))


def inscripcion_por_id(identificador):
    return Inscripcion.get_or_none(Inscripcion.id == identificador)


def inscripcion_existente(estudiante_id, curso_id):
    return Inscripcion.get_or_none(
        (Inscripcion.estudiante == estudiante_id) & (Inscripcion.curso == curso_id)
    )


def cupos_ocupados(curso_id):
    return Inscripcion.select().where(
        (Inscripcion.curso == curso_id) & (Inscripcion.estado != 'Cancelada')
    ).count()


def guardar_inscripcion(inscripcion):
    inscripcion.save()
    return inscripcion
