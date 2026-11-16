from datos.modelos.persona import Instructor
from datos.repositorio.repositorio_cursos import curso_por_id, listado_cursos
from datos.repositorio.repositorio_inscripciones import cupos_ocupados
from negocio.negocio_cursos import cambiar_estado_curso, guardar_datos_curso
from presentacion.presentacion_personas import mostrar_personas
from presentacion.utilidades import mostrar_tabla, pedir_campo, pedir_id, submenu


def mostrar_cursos():
    mostrar_tabla(
        ['ID', 'Curso', 'Instructor', 'Horas', 'Precio CLP', 'Cupos libres', 'Habilitado'],
        ([curso.id, curso.titulo, curso.instructor.nombre, curso.duracion_horas,
          f'${curso.precio:,.2f}', curso.cupos - cupos_ocupados(curso.id),
          'Sí' if curso.habilitado else 'No'] for curso in listado_cursos()),
    )


def formulario_curso(editar=False):
    curso = None
    if editar:
        mostrar_cursos()
        curso = curso_por_id(pedir_id())
        if curso is None:
            raise ValueError('No existe un curso con ese ID.')
    titulo = pedir_campo('Título', curso.titulo if curso else None)
    descripcion = pedir_campo('Descripción', curso.descripcion if curso else None)
    mostrar_personas(Instructor)
    instructor_id = pedir_campo('ID del instructor', curso.instructor_id if curso else None)
    duracion = pedir_campo('Duración en horas', curso.duracion_horas if curso else None)
    precio = pedir_campo('Precio en CLP (0 para gratuito)', curso.precio if curso else None)
    cupos = pedir_campo('Cupos totales', curso.cupos if curso else None)
    guardado = guardar_datos_curso(
        titulo, descripcion, instructor_id, duracion, precio, cupos,
        curso.id if curso else None,
    )
    print(f'Curso guardado con ID {guardado.id}.')


def presentar_detalle():
    curso = curso_por_id(pedir_id('ID del curso: '))
    if curso is None:
        raise ValueError('No existe un curso con ese ID.')
    print(f'\n{curso.titulo}\n{curso.descripcion}')
    print(f'Instructor: {curso.instructor.nombre} | Duración: {curso.duracion_horas} horas')
    print(f'Precio: ${curso.precio:,.2f} CLP | Cupos totales: {curso.cupos}')
    print(f'Cupos disponibles: {curso.cupos - cupos_ocupados(curso.id)}')


def presentar_estado():
    mostrar_cursos()
    curso = cambiar_estado_curso(pedir_id())
    print(f'Curso {"habilitado" if curso.habilitado else "deshabilitado"}.')


def menu_cursos():
    submenu('Cursos', {
        '1': ('Listar cursos', mostrar_cursos),
        '2': ('Crear curso', formulario_curso),
        '3': ('Editar curso', lambda: formulario_curso(editar=True)),
        '4': ('Habilitar / deshabilitar curso', presentar_estado),
        '5': ('Ver detalle de un curso', presentar_detalle),
    })
