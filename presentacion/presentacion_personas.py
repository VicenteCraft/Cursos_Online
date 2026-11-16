from datos.modelos.persona import Estudiante, Instructor
from datos.repositorio.repositorio_personas import listado_personas, persona_por_id
from negocio.negocio_personas import cambiar_estado_persona, guardar_datos_persona
from presentacion.utilidades import mostrar_tabla, pedir_campo, pedir_id, submenu


def mostrar_personas(modelo):
    columnas = ['ID', 'Nombre', 'Correo', 'Habilitado']
    if modelo is Instructor:
        columnas.insert(3, 'Especialidad')
    filas = []
    for persona in listado_personas(modelo):
        fila = [persona.id, persona.nombre, persona.correo]
        if modelo is Instructor:
            fila.append(persona.especialidad)
        fila.append('Sí' if persona.habilitado else 'No')
        filas.append(fila)
    mostrar_tabla(columnas, filas)


def formulario_persona(modelo, editar=False):
    persona = None
    if editar:
        mostrar_personas(modelo)
        persona = persona_por_id(modelo, pedir_id())
        if persona is None:
            raise ValueError('No existe una persona con ese ID.')
    nombre = pedir_campo('Nombre completo', persona.nombre if persona else None)
    correo = pedir_campo('Correo electrónico', persona.correo if persona else None)
    especialidad = None
    if modelo is Instructor:
        especialidad = pedir_campo('Especialidad', persona.especialidad if persona else None)
    guardada = guardar_datos_persona(
        modelo, nombre, correo, especialidad, persona.id if persona else None,
    )
    print(f'{guardada.descripcion()} guardado/a con ID {guardada.id}.')


def presentar_estado(modelo):
    mostrar_personas(modelo)
    persona = cambiar_estado_persona(modelo, pedir_id())
    print(f'{persona.nombre}: {"habilitado/a" if persona.habilitado else "deshabilitado/a"}.')


def menu_personas(modelo):
    titulo = 'Estudiantes' if modelo is Estudiante else 'Instructores'
    submenu(titulo, {
        '1': ('Listar', lambda: mostrar_personas(modelo)),
        '2': ('Registrar', lambda: formulario_persona(modelo)),
        '3': ('Editar', lambda: formulario_persona(modelo, editar=True)),
        '4': ('Habilitar / deshabilitar', lambda: presentar_estado(modelo)),
    })
