import re
from decimal import Decimal, InvalidOperation


def texto_obligatorio(valor, campo):
    valor = str(valor).strip()
    if not valor:
        raise ValueError(f'El campo {campo} es obligatorio.')
    if len(valor) > 150:
        raise ValueError(f'El campo {campo} admite hasta 150 caracteres.')
    return valor


def validar_correo(correo):
    correo = texto_obligatorio(correo, 'correo').lower()
    if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', correo):
        raise ValueError('El correo electrónico no tiene un formato válido.')
    return correo


def entero_positivo(valor, campo):
    try:
        numero = int(str(valor))
    except (TypeError, ValueError):
        raise ValueError(f'{campo} debe ser un número entero.') from None
    if numero <= 0:
        raise ValueError(f'{campo} debe ser mayor que cero.')
    return numero


def validar_precio(valor):
    try:
        precio = Decimal(str(valor).replace(',', '.'))
        if not precio.is_finite() or precio < 0 or precio > Decimal('9999999999.99'):
            raise ValueError
        redondeado = precio.quantize(Decimal('0.01'))
        if redondeado != precio:
            raise ValueError
        return redondeado
    except (InvalidOperation, ValueError):
        raise ValueError('El precio debe ser positivo o cero y tener hasta 2 decimales.') from None


def validar_progreso(valor):
    try:
        progreso = int(str(valor))
    except (TypeError, ValueError):
        raise ValueError('El progreso debe ser un número entero.') from None
    if not 0 <= progreso <= 100:
        raise ValueError('El progreso debe estar entre 0 y 100.')
    return progreso
