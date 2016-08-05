# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.utils.text import slugify
from .models import Encuesta, Pregunta, Respuesta
from .model_utils import crear_encuesta, modificar_encuesta, contestar_encuesta


# Create your tests here.
class TestCrudEncuestas(TestCase):
    def setUp(self):
        self.cliente = Client()

    def test_crear_encuesta(self):
        request_json_encuesta = {
            'titulo': 'Pasa la prueba del test',
            'encabezado': 'Encabezado de prueba',
            'publicada': 'true',
            'abierta': 'true',
            'preguntas': [
                {'texto': '¿Funciona el agregado de preguntas?', 'opciones': ['si', 'no']},
                {'texto': '¿Preguntas abiertas en una encuesta?'}
            ]
        }

        encuesta_creada = crear_encuesta(request_json_encuesta['titulo'], request_json_encuesta['encabezado'], request_json_encuesta['preguntas'], request_json_encuesta['publicada'], request_json_encuesta['abierta'])
        self.assertIsInstance(encuesta_creada, Encuesta)
        encuesta_creada.delete()

    def test_modificar_encuesta(self):
        request_json_encuesta = {
            'titulo': 'Pasa la prueba del test',
            'encabezado': 'Encabezado de prueba',
            'publicada': 'true',
            'abierta': 'true',
            'preguntas': [
                {'texto': '¿Funciona el agregado de preguntas?', 'opciones': ['si', 'no']},
                {'texto': '¿Preguntas abiertas en una encuesta?'}
            ]
        }

        encuesta_creada = crear_encuesta(request_json_encuesta['titulo'], request_json_encuesta['encabezado'], request_json_encuesta['preguntas'], request_json_encuesta['publicada'], request_json_encuesta['abierta'])
        request_json_encuesta_mod = {
            'titulo': 'Pasa la prueba del test',
            'encabezado': 'Encabezado de pruebas',
            'publicada': 'false',
            'abierta': 'false',
            'preguntas': [
                {'texto': '¿Funciona el agregado de preguntas?', 'opciones': ['si', 'no']},
                {'texto': '¿Preguntas abiertas en una encuesta?'},
                {'texto': '¿Preguntas abiertas en una encuesta 2?'}
            ]
        }

        encuesta_creada = modificar_encuesta(encuesta_creada.id, request_json_encuesta_mod['titulo'], request_json_encuesta_mod['encabezado'], request_json_encuesta_mod['preguntas'], request_json_encuesta_mod['publicada'], request_json_encuesta_mod['abierta'])

        self.assertEquals(len(encuesta_creada.preguntas), 3)
        self.assertEquals(encuesta_creada.publicada, False)
        self.assertEquals(encuesta_creada.abierta, False)
        self.assertEquals(encuesta_creada.encabezado, 'Encabezado de pruebas')
        self.assertIsInstance(encuesta_creada, Encuesta)

    def test_responder_encuesta(self):
        Encuesta.objects.filter(slug=slugify('Pasa la prueba del test')).delete()
        request_json_encuesta = {
            'titulo': 'Pasa la prueba del test',
            'encabezado': 'Encabezado de prueba',
            'publicada': 'true',
            'abierta': 'true',
            'preguntas': [
                {'texto': '¿Funciona el agregado de preguntas?', 'opciones': ['si', 'no']},
                {'texto': '¿Preguntas abiertas en una encuesta?'}
            ]
        }

        encuesta_creada = crear_encuesta(request_json_encuesta['titulo'], request_json_encuesta['encabezado'], request_json_encuesta['preguntas'], request_json_encuesta['publicada'], request_json_encuesta['abierta'])

        request_respuestas = [
            {'pregunta': '¿Funciona el agregado de preguntas?', 'valor': 0},
            {'pregunta': '¿Preguntas abiertas en una encuesta?', 'valor': 'No por supuesto que no'},
        ]

        encuesta_creada = contestar_encuesta(slugify('Pasa la prueba del test'), request_respuestas)

        request_respuestas = [
            {'pregunta': '¿Funciona el agregado de preguntas?', 'valor': 1},
            {'pregunta': '¿Preguntas abiertas en una encuesta?', 'valor': 'Si claro que si'},
        ]

        encuesta_creada = contestar_encuesta(slugify('Pasa la prueba del test'), request_respuestas)

        # print encuesta_creada.respuestas
        encuesta = Encuesta.objects.first()
        self.assertEquals(len(encuesta.respuestas), 4)
