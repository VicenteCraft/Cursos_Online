from peewee import DatabaseError
from prettytable import PrettyTable

from auxiliares.validaciones import entero_positivo


def mostrar_tabla(columnas, filas):
    tabla = PrettyTable()
    tabla.field_names = columnas
    tabla.align = 'l'
    tabla.max_width = 40
    for fila in filas:
        tabla.add_row(fila)
    print(tabla)
    if not tabla.rows:
        print('No hay registros para mostrar.')


def pedir_id(mensaje='ID: '):
    return entero_positivo(input(mensaje), 'ID')


def pedir_campo(mensaje, actual=None):
    if actual is None:
        return input(f'{mensaje}: ').strip()
    valor = input(f'{mensaje} [{actual}] (Enter para conservar): ').strip()
    return valor if valor else actual


def ejecutar_accion(accion):
    try:
        accion()
    except ValueError as error:
        print(f'\nNo se pudo realizar la operación: {error}')
    except DatabaseError as error:
        print(f'\nError de base de datos: {error}')


def submenu(titulo, acciones):
    while True:
        print(f'\n--- {titulo} ---')
        for clave, (etiqueta, _) in acciones.items():
            print(f'[{clave}] {etiqueta}')
        print('[0] Volver')
        opcion = input('Seleccione una opción: ').strip()
        if opcion == '0':
            return
        if opcion in acciones:
            ejecutar_accion(acciones[opcion][1])
        else:
            print('Opción no válida.')
