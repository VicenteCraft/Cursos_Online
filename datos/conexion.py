from pathlib import Path

from decouple import AutoConfig
from peewee import MySQLDatabase, SqliteDatabase


RAIZ = Path(__file__).resolve().parent.parent
config = AutoConfig(search_path=str(RAIZ))


def base_datos():
    motor = config('DB_MOTOR', default='sqlite').lower()
    if motor == 'mysql':
        return MySQLDatabase(
            config('DB_NOMBRE', default='cursos_online'),
            host=config('DB_HOST', default='localhost'),
            port=config('DB_PUERTO', default=3306, cast=int),
            user=config('DB_USUARIO', default='root'),
            password=config('DB_PASSWORD', default=''),
            charset='utf8mb4',
        )
    if motor != 'sqlite':
        raise ValueError('DB_MOTOR debe ser sqlite o mysql.')
    archivo = Path(config('DB_ARCHIVO', default='cursos_online.db'))
    if not archivo.is_absolute():
        archivo = RAIZ / archivo
    return SqliteDatabase(str(archivo), pragmas={'foreign_keys': 1}, timeout=10)


database = base_datos()
