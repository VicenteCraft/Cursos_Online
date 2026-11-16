# Academia Online

Proyecto de **Programación Orientada a Objetos en Python**, basado en la organización del proyecto de biblioteca de la carpeta `IEC_N2_C2_POO-main` y adaptado a la gestión de cursos online.

La aplicación funciona mediante **menús de consola** y guarda los datos en una base de datos usando el ORM **Peewee**.

## Funcionalidades

- Inicio de sesión de administración y cambio de contraseña.
- Registro, listado, edición y habilitación/deshabilitación de estudiantes e instructores.
- Creación, listado, consulta de detalle, edición y habilitación/deshabilitación de cursos.
- Cursos con descripción, instructor, duración, precio en pesos chilenos y cupos.
- Inscripción de estudiantes con control de cupos y prevención de duplicados.
- Seguimiento del progreso de 0 a 100 %. Al llegar a 100 %, la inscripción queda completada.
- Cancelación de inscripciones y liberación de cupos.
- Reinscripción de una inscripción cancelada, reiniciando su progreso y fecha.
- Consulta de inscripciones por estudiante y resumen general de la academia.
- Persistencia automática en SQLite y configuración opcional de MySQL.

## Requisitos e instalación

Necesitas Python 3.10 o superior. Abre una terminal dentro de `Cursos_Online` y ejecuta:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

También puedes instalar las dependencias en tu entorno Python actual:

```powershell
python -m pip install -r requirements.txt
python main.py
```

### Acceso inicial

| Campo | Valor |
| --- | --- |
| Usuario | `admin` |
| Contraseña | `Admin123!` |

Las contraseñas se almacenan como hashes PBKDF2 con sal. Puedes cambiar la contraseña en la opción **6** del menú principal.

En la primera ejecución se crean las tablas, el administrador, una instructora y dos cursos de ejemplo. Los ejemplos no se vuelven a insertar en los siguientes inicios. La base de datos `cursos_online.db` se guarda dentro de la carpeta del proyecto, independientemente de desde dónde ejecutes `main.py`.

## Ejemplo de uso

1. Inicia sesión con el administrador.
2. En **Gestionar estudiantes → Registrar**, ingresa un nombre y correo.
3. En **Gestionar cursos → Listar cursos**, consulta los cursos de ejemplo y sus IDs.
4. En **Gestionar inscripciones y progreso → Inscribir estudiante**, ingresa el ID del estudiante y el ID del curso.
5. En **Actualizar progreso**, selecciona la inscripción e indica un porcentaje.
6. Consulta el resumen general desde la opción **5** del menú principal.

En los formularios de edición, presiona Enter para conservar un valor. La opción **0** permite volver al menú anterior o salir.

## Estructura por capas

```text
Cursos_Online/
├── main.py                    # Inicio, conexión e inicio de sesión
├── requirements.txt
├── .env.example               # Ejemplo de configuración
├── auxiliares/                # Validaciones y contraseñas
├── datos/
│   ├── conexion.py            # Selección SQLite/MySQL
│   ├── inicializacion.py      # Creación de tablas y ejemplos
│   ├── modelos/               # Clases persistentes de Peewee
│   └── repositorio/           # Consultas y operaciones de persistencia
├── negocio/                   # Reglas y validaciones de la aplicación
├── presentacion/              # Menús y tablas de consola
└── tests/                     # Pruebas de integración en memoria
```

### Programación orientada a objetos

- **Herencia:** `Estudiante` e `Instructor` heredan los atributos comunes de `Persona`; las entidades persistentes derivan de `ModeloBase`.
- **Polimorfismo:** ambos tipos de persona implementan `descripcion()` con un comportamiento propio.
- **Relaciones:** cada curso pertenece a un instructor; cada inscripción relaciona un estudiante con un curso.
- **Separación de responsabilidades:** presentación solicita y muestra información, negocio aplica las reglas y repositorio accede a los datos.

`Persona` se utiliza como clase base; se crean tablas independientes para estudiantes e instructores.

### Reglas principales

- Los correos deben tener formato válido y ser únicos dentro de cada tipo de persona.
- Los títulos de cursos son únicos; duración y cupos deben ser enteros mayores que cero.
- El precio admite cero (curso gratuito) y hasta dos decimales.
- Solo se permite inscribir estudiantes habilitados en cursos habilitados con instructor habilitado.
- Una inscripción completada conserva su cupo como parte de la matrícula histórica del curso.
- El progreso no puede disminuir; las inscripciones completadas se conservan y no pueden cancelarse.
- Deshabilitar una entidad conserva su historial y bloquea nuevas inscripciones relacionadas; no cancela automáticamente las existentes.
- La baja de estudiantes, instructores y cursos es lógica mediante el campo `habilitado`.

## MySQL opcional

1. Crea una base de datos en MySQL:

   ```sql
   CREATE DATABASE cursos_online CHARACTER SET utf8mb4;
   ```

2. Crea un archivo `.env` dentro de `Cursos_Online`, tomando `.env.example` como referencia:

   ```dotenv
   DB_MOTOR=mysql
   DB_NOMBRE=cursos_online
   DB_HOST=localhost
   DB_PUERTO=3306
   DB_USUARIO=tu_usuario
   DB_PASSWORD=tu_contrasenia
   ```

3. Ejecuta `python main.py`. Peewee crea las tablas y relaciones automáticamente. El usuario configurado debe tener permisos de creación de tablas, lectura y escritura en esa base.

SQLite y MySQL mantienen bases independientes; cambiar de motor no migra datos. Para SQLite no es necesario crear un archivo `.env`.

## Verificación

Desde la carpeta del proyecto:

```powershell
python -m unittest discover -s tests -v
```

Las pruebas usan SQLite en memoria y verifican autenticación, persistencia, cupos, duplicados, cancelación, reinscripción, progreso y restricciones de edición sin modificar tu base de datos.
