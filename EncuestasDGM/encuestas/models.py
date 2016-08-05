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


class Encuesta(Document):
    titulo = StringField(max_length=200, required=True)
    slug = StringField(max_length=250, required=True)
    encabezado = StringField(max_length=500, required=True)
    fecha = DateTimeField(dafault=datetime.now())
    publicada = BooleanField(default=False)
    abierta = BooleanField(default=False)
    preguntas = ListField(EmbeddedDocumentField(Pregunta))
    respuestas = ListField(EmbeddedDocumentField(Respuesta), required=False)