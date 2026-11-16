from auxiliares.seguridad import generar_hash, verificar_contrasenia
from auxiliares.validaciones import texto_obligatorio
from datos.modelos.usuario import Usuario


def autenticar_usuario(nombre, contrasenia):
    usuario = Usuario.get_or_none(Usuario.nombre == nombre.strip())
    if usuario and verificar_contrasenia(contrasenia, usuario.password_hash):
        return usuario
    return None


def cambiar_contrasenia(usuario, actual, nueva):
    if not verificar_contrasenia(actual, usuario.password_hash):
        raise ValueError('La contraseña actual no es correcta.')
    usuario.password_hash = generar_hash(nueva)
    usuario.save()


def crear_usuario(nombre, contrasenia):
    return Usuario.create(
        nombre=texto_obligatorio(nombre, 'usuario'),
        password_hash=generar_hash(contrasenia),
    )
