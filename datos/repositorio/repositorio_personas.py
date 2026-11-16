def listado_personas(modelo):
    return modelo.select().order_by(modelo.nombre)


def persona_por_id(modelo, identificador):
    return modelo.get_or_none(modelo.id == identificador)


def guardar_persona(persona):
    persona.save()
    return persona
