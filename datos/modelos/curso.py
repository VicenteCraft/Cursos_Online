from peewee import AutoField, BooleanField, CharField, DecimalField, ForeignKeyField, IntegerField

from datos.modelos.base import ModeloBase
from datos.modelos.persona import Instructor


class Curso(ModeloBase):
    id = AutoField()
    titulo = CharField(max_length=150, unique=True)
    descripcion = CharField(max_length=150)
    instructor = ForeignKeyField(Instructor, backref='cursos', on_delete='RESTRICT')
    duracion_horas = IntegerField()
    precio = DecimalField(max_digits=12, decimal_places=2, auto_round=True)
    cupos = IntegerField()
    habilitado = BooleanField(default=True)

    class Meta:
        table_name = 'cursos'
