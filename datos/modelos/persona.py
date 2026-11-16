from datetime import datetime

from peewee import AutoField, BooleanField, CharField, DateTimeField

from datos.modelos.base import ModeloBase


class Persona(ModeloBase):
    id = AutoField()
    nombre = CharField(max_length=150)
    correo = CharField(max_length=150, unique=True)
    habilitado = BooleanField(default=True)
    fecha_registro = DateTimeField(default=datetime.now)

    def descripcion(self):
        return self.nombre


class Estudiante(Persona):
    def descripcion(self):
        return f'Estudiante: {self.nombre}'

    class Meta:
        table_name = 'estudiantes'


class Instructor(Persona):
    especialidad = CharField(max_length=150)

    def descripcion(self):
        return f'Instructor: {self.nombre} ({self.especialidad})'

    class Meta:
        table_name = 'instructores'
