from peewee import IntegrityError

from auxiliares.validaciones import entero_positivo, texto_obligatorio, validar_precio
from datos.modelos.curso import Curso
from datos.modelos.persona import Instructor
from datos.repositorio.repositorio_cursos import curso_por_id, guardar_curso
from datos.repositorio.repositorio_inscripciones import cupos_ocupados
from datos.repositorio.repositorio_personas import persona_por_id


def guardar_datos_curso(titulo, descripcion, instructor_id, duracion, precio, cupos,
                        identificador=None):
    curso = Curso() if identificador is None else curso_por_id(identificador)
    if curso is None:
        raise ValueError('No existe un curso con ese ID.')
    instructor = persona_por_id(Instructor, entero_positivo(instructor_id, 'ID de instructor'))
    if instructor is None or not instructor.habilitado:
        raise ValueError('Debes seleccionar un instructor habilitado.')
    curso.titulo = texto_obligatorio(titulo, 'título')
    curso.descripcion = texto_obligatorio(descripcion, 'descripción')
    curso.instructor = instructor
    curso.duracion_horas = entero_positivo(duracion, 'Duración')
    curso.precio = validar_precio(precio)
    curso.cupos = entero_positivo(cupos, 'Cupos')
    if curso.id and curso.cupos < cupos_ocupados(curso.id):
        raise ValueError('Los cupos no pueden ser menores que las inscripciones vigentes.')
    try:
        return guardar_curso(curso)
    except IntegrityError:
        raise ValueError('Ya existe un curso con ese título.') from None


def cambiar_estado_curso(identificador):
    curso = curso_por_id(identificador)
    if curso is None:
        raise ValueError('No existe un curso con ese ID.')
    curso.habilitado = not curso.habilitado
    return guardar_curso(curso)
