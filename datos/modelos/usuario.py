from peewee import AutoField, CharField

from datos.modelos.base import ModeloBase


class Usuario(ModeloBase):
    id = AutoField()
    nombre = CharField(max_length=150, unique=True)
    password_hash = CharField(max_length=200)

    class Meta:
        table_name = 'usuarios'
