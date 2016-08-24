from __future__ import unicode_literals
from datetime import datetime
from mongoengine import *


# Create your models here.
class Pregunta(EmbeddedDocument):
    texto = StringField(max_length=500, required=True)
    opciones = ListField(StringField(max_length=50), required=False)


class Respuesta(EmbeddedDocument):
    pregunta = StringField(max_length=300, required=True)
    valor = StringField(max_length=500, required=False)
    fecha = DateTimeField(default=datetime.now())
    hash_respuesta = StringField(max_length=200)

    def save(self, *args, **kwargs):
        if not self.fecha:
            self.fecha = datetime.now()

        return super(Respuesta, self).save(*args, **kwargs)

class Encuesta(Document):
    titulo = StringField(max_length=200, required=True)
    slug = StringField(max_length=250, required=True)
    encabezado = StringField(max_length=500, required=True)
    fecha_creacion = DateTimeField(default=datetime.now())
    fecha_modificacion = DateTimeField(default=datetime.now())
    publicada = BooleanField(default=False)
    abierta = BooleanField(default=False)
    preguntas = ListField(EmbeddedDocumentField(Pregunta))
    respuestas = ListField(EmbeddedDocumentField('Respuesta'), required=False)

    def save(self, *args, **kwargs):
        if not self.fecha_creacion:
            self.fecha_creacion = datetime.now()
        self.fecha_modificacion = datetime.now()

        return super(Encuesta, self).save(*args, **kwargs)
