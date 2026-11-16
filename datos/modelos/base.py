from peewee import Model

from datos.conexion import database


class ModeloBase(Model):
    class Meta:
        database = database
