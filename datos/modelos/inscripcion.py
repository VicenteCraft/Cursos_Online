from datetime import datetime

from peewee import AutoField, CharField, DateTimeField, ForeignKeyField, IntegerField

from datos.modelos.base import ModeloBase
from datos.modelos.curso import Curso
from datos.modelos.persona import Estudiante


class Inscripcion(ModeloBase):
    id = AutoField()
    estudiante = ForeignKeyField(Estudiante, backref='inscripciones', on_delete='RESTRICT')
    curso = ForeignKeyField(Curso, backref='inscripciones', on_delete='RESTRICT')
    fecha_inscripcion = DateTimeField(default=datetime.now)
    progreso = IntegerField(default=0)
    estado = CharField(max_length=20, default='Activa')

    class Meta:
        table_name = 'inscripciones'
        indexes = ((('estudiante', 'curso'), True),)
