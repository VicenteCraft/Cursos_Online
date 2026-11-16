from getpass import getpass

from negocio.negocio_usuarios import autenticar_usuario, cambiar_contrasenia


def login_usuario():
    print('Inicia sesión con tu cuenta de administración. Escribe 0 para salir.')
    while True:
        nombre = input('Usuario: ').strip()
        if nombre == '0':
            return None
        usuario = autenticar_usuario(nombre, getpass('Contraseña: '))
        if usuario:
            print(f'\nBienvenido/a, {usuario.nombre}.')
            return usuario
        print('Usuario o contraseña incorrectos.')


def presentar_cambio_contrasenia(usuario):
    actual = getpass('Contraseña actual: ')
    nueva = getpass('Nueva contraseña (mínimo 8 caracteres): ')
    if nueva != getpass('Repite la nueva contraseña: '):
        raise ValueError('Las contraseñas nuevas no coinciden.')
    cambiar_contrasenia(usuario, actual, nueva)
    print('Contraseña actualizada.')
