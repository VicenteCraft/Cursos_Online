from peewee import IntegrityError

from auxiliares.validaciones import texto_obligatorio, validar_correo
from datos.modelos.persona import Estudiante, Instructor
from datos.repositorio.repositorio_personas import guardar_persona, persona_por_id


def guardar_datos_persona(modelo, nombre, correo, especialidad=None, identificador=None):
    if modelo not in (Estudiante, Instructor):
        raise ValueError('Tipo de persona no válido.')
    persona = modelo() if identificador is None else persona_por_id(modelo, identificador)
    if persona is None:
        raise ValueError('No existe una persona con ese ID.')
    persona.nombre = texto_obligatorio(nombre, 'nombre')
    persona.correo = validar_correo(correo)
    if modelo is Instructor:
        persona.especialidad = texto_obligatorio(especialidad or '', 'especialidad')
    try:
        return guardar_persona(persona)
    except IntegrityError:
        raise ValueError('Ya existe un registro con ese correo.') from None


def cambiar_estado_persona(modelo, identificador):
    persona = persona_por_id(modelo, identificador)
    if persona is None:
        raise ValueError('No existe una persona con ese ID.')
    persona.habilitado = not persona.habilitado
    return guardar_persona(persona)
