from __future__ import unicode_literals
import json
from collections import OrderedDict
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

    def devuelve_respuestas(self):
        preguntas = { pregunta.texto: pregunta for pregunta in self.preguntas}
        preguntas_resultados = { pregunta.texto: {'pregunta': None, 'valores': [], 'opciones': None} for pregunta in self.preguntas}

        for respuesta in self.respuestas:
            preguntas_resultados[respuesta.pregunta]['abierta'] = True if len(preguntas[respuesta.pregunta].opciones) == 0 else False
            preguntas_resultados[respuesta.pregunta]['opciones'] = preguntas[respuesta.pregunta].opciones
            preguntas_resultados[respuesta.pregunta]['valores'].append(respuesta.valor)

        return preguntas_resultados

    def devuelve_respuestas_abiertas(self):
        preguntas = { pregunta.texto: pregunta for pregunta in self.preguntas}
        preguntas_resultados = { pregunta.texto: [] for pregunta in self.preguntas}

        for respuesta in self.respuestas:
            if len(preguntas[respuesta.pregunta].opciones) == 0:
                preguntas_resultados[respuesta.pregunta].append(respuesta.valor)

        return preguntas_resultados

    def devuelve_respuestas_cerradas(self):
        preguntas_array = []
        preguntas = { pregunta.texto: pregunta for pregunta in self.preguntas}
        preguntas_resultados = { pregunta.texto: [] for pregunta in self.preguntas}

        for respuesta in self.respuestas:
            if len(preguntas[respuesta.pregunta].opciones) > 0:
                preguntas_resultados[respuesta.pregunta].append(respuesta.valor)

        for pregunta in self.preguntas:
            if len(pregunta.opciones) > 0:
                pregunta_aux = OrderedDict()
                pregunta_aux["label"] = pregunta.texto
                pregunta_aux["valoresarray"] = None

                for opcion in pregunta.opciones:
                    pregunta_aux[opcion] = 0

                preguntas_array.append(pregunta_aux)

        respuesta_de_barchart = {
          "ejex": "Preguntas",
          "ejey": "Respuestas",
          "valores": preguntas_array
        }

        counter = 0
        for pregunta in preguntas_resultados.keys():
            for resultado in preguntas_resultados[pregunta]:
                for valores in respuesta_de_barchart['valores']:
                    if valores['label'] == pregunta:
                        valores[preguntas[pregunta].opciones[int(resultado) - 1]] += 1

        elemento_aux = []

        for elemento in respuesta_de_barchart['valores']:
            elemento_aux.append([elemento['label'], 'valor'])
            for opcion in elemento.keys():
                if opcion != 'label' and opcion != 'valoresarray' and opcion:
                    elemento_aux.append([opcion, elemento[opcion]])
            elemento['valoresarray'] = json.dumps(elemento_aux)
            counter += 1

        return respuesta_de_barchart

    def save(self, *args, **kwargs):
        if not self.fecha_creacion:
            self.fecha_creacion = datetime.now()
        self.fecha_modificacion = datetime.now()

        return super(Encuesta, self).save(*args, **kwargs)
