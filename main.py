from peewee import OperationalError

from datos.conexion import database
from datos.inicializacion import inicializar_datos
from presentacion.menu import menu_principal
from presentacion.presentacion_usuarios import login_usuario


def main():
    try:
        database.connect(reuse_if_open=True)
        inicializar_datos()
        print('\nACADEMIA ONLINE - Gestión de cursos')
        usuario = login_usuario()
        if usuario:
            menu_principal(usuario)
    except (KeyboardInterrupt, EOFError):
        print('\nSesión finalizada.')
    except OperationalError as error:
        print(f'No fue posible acceder a la base de datos: {error}')
        print('Revisa la configuración indicada en README.md.')
    finally:
        if not database.is_closed():
            database.close()


if __name__ == '__main__':
    main()
