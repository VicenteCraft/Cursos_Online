from datos.modelos.curso import Curso
from datos.modelos.persona import Instructor


def listado_cursos():
    return Curso.select(Curso, Instructor).join(Instructor).order_by(Curso.titulo)


def curso_por_id(identificador):
    return Curso.get_or_none(Curso.id == identificador)


def guardar_curso(curso):
    curso.save()
    return curso
