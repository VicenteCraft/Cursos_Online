import hashlib
import hmac
import secrets


def generar_hash(contrasenia):
    if len(contrasenia) < 8:
        raise ValueError('La contraseña debe tener al menos 8 caracteres.')
    sal = secrets.token_hex(16)
    resumen = hashlib.pbkdf2_hmac('sha256', contrasenia.encode(), sal.encode(), 260000)
    return f'{sal}${resumen.hex()}'


def verificar_contrasenia(contrasenia, hash_guardado):
    sal, resumen = hash_guardado.split('$', 1)
    candidato = hashlib.pbkdf2_hmac('sha256', contrasenia.encode(), sal.encode(), 260000)
    return hmac.compare_digest(candidato.hex(), resumen)
