# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.utils.text import slugify
from django.contrib.auth.models import User
from .models import Encuesta, Pregunta, Respuesta
from .model_utils import crear_encuesta, modificar_encuesta, contestar_encuesta


# Create your tests here.
class TestCrudEncuestas(TestCase):
    def setUp(self):
        self.cliente = Client()

    def tearDown(self):
        Encuesta.objects.filter(slug__startswith=slugify('Pasa la prueba del test')).delete()

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

        encuesta_creada = modificar_encuesta(encuesta_creada, request_json_encuesta_mod['titulo'], request_json_encuesta_mod['encabezado'], request_json_encuesta_mod['preguntas'], request_json_encuesta_mod['publicada'], request_json_encuesta_mod['abierta'])

        self.assertEquals(len(encuesta_creada.preguntas), 3)
        self.assertEquals(encuesta_creada.publicada, False)
        self.assertEquals(encuesta_creada.abierta, False)
        self.assertEquals(encuesta_creada.encabezado, 'Encabezado de pruebas')
        self.assertIsInstance(encuesta_creada, Encuesta)

    def test_responder_encuesta(self):
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
            {'pregunta': u'¿Funciona el agregado de preguntas?', 'valor': 0},
            {'pregunta': u'¿Preguntas abiertas en una encuesta?', 'valor': 'No por supuesto que no'},
        ]

        encuesta_creada = contestar_encuesta(encuesta_creada, request_respuestas)

        request_respuestas = [
            {'pregunta': u'¿Funciona el agregado de preguntas?', 'valor': 1},
            {'pregunta': u'¿Preguntas abiertas en una encuesta?', 'valor': 'Si claro que si'},
        ]

        encuesta_creada = contestar_encuesta(encuesta_creada, request_respuestas)

        # print encuesta_creada.respuestas
        encuesta = Encuesta.objects.get(slug=encuesta_creada.slug)
        self.assertEquals(len(encuesta.respuestas), 4)


class TestCRUDHttp(TestCase):
    def setUp(self):
        self.cliente = Client()
        # Creando usuario test para pruebas
        user = User.objects.create_user(username='test', password='test')
        user.is_staff = True
        user.save()

    def tearDown(self):
        Encuesta.objects.filter(slug__startswith=slugify('Pasa la prueba del test')).delete()

    def login_user_test(self):
        self.cliente.login(username='test', password='test')

    def test_admin_crear_encuesta(self):
        """
        Test que prueba los escenarios
        y validaciones de la creacion
        de encuestas
        """
        self.login_user_test()
        # Probar que se visualiza la pagina logueado
        self.assertTrue(self.cliente.login(username='test', password='test'))
        respuesta = self.cliente.get('http://0.0.0.0:8000/encuestas/administrador/crear-encuesta/')
        self.assertEquals(respuesta.status_code, 200)
        
        request_json_encuesta = {
            'titulo': "Pasa la prueba del test",
            'encabezado': "Encabezado de prueba",
            'publicada': "on",
            'abierta': "on",
            'preguntas': '[{"texto": "¿Funciona el agregado de preguntas?", "opciones": ["si", "no"]}, {"texto": "¿Preguntas abiertas en una encuesta?", "opciones": [  ]}]'
        }

        # Probando creacion de una encuesta
        respuesta = self.cliente.post('http://0.0.0.0:8000/encuestas/administrador/crear-encuesta/', request_json_encuesta)
        self.assertEquals(respuesta.status_code, 200)
        self.assertEquals(respuesta.json()['estatus'], u'ok')

        # Probando validacion de titulo para creacion de encuestas
        request_json_encuesta['titulo'] = ''
        respuesta = self.cliente.post('http://0.0.0.0:8000/encuestas/administrador/crear-encuesta/', request_json_encuesta)
        self.assertEquals(respuesta.status_code, 200)
        self.assertEquals(respuesta.json()['estatus'], u'error')
        self.assertEquals(respuesta.json()['error'], u'Se necesita un titulo para crear la encuesta')
        request_json_encuesta['titulo'] = 'test'

        # Probando validacion de encabezado para creacion de encuestas
        request_json_encuesta['encabezado'] = ''
        respuesta = self.cliente.post('http://0.0.0.0:8000/encuestas/administrador/crear-encuesta/', request_json_encuesta)
        self.assertEquals(respuesta.status_code, 200)
        self.assertEquals(respuesta.json()['estatus'], u'error')
        self.assertEquals(respuesta.json()['error'], u'Se necesita un encabezado para crear la encuesta')
        request_json_encuesta['encabezado'] = 'test'

        # Probando validacion de preguntas para creacion de encuestas
        request_json_encuesta['preguntas'] = '[]'
        respuesta = self.cliente.post('http://0.0.0.0:8000/encuestas/administrador/crear-encuesta/', request_json_encuesta)
        self.assertEquals(respuesta.status_code, 200)
        self.assertEquals(respuesta.json()['estatus'], u'error')
        self.assertEquals(respuesta.json()['error'], u'Se necesita al menos una pregunta para crear la encuesta')
        request_json_encuesta['preguntas'] = '[{"texto": "¿Funciona el agregado de preguntas?", "opciones": ["si", "no"]}, {"texto": "¿Preguntas abiertas en una encuesta?", "opciones": [  ]}]'

    def test_admin_modificar_encuesta(self):
        """
        Test que prueba los escenarios
        y validaciones dentro del end point
        para edicon de encuestas
        """
        self.login_user_test()
        # Probar que se visualiza la pagina logueado
        self.assertTrue(self.cliente.login(username='test', password='test'))
        respuesta = self.cliente.get('http://0.0.0.0:8000/encuestas/administrador/editar-encuesta/pasa-la-prueba-del-test/')
        self.assertEquals(respuesta.status_code, 200)
        
        request_json_encuesta = {
            'titulo': "Pasa la prueba del test",
            'encabezado': "Encabezado de prueba",
            'publicada': "on",
            'abierta': "on",
            'preguntas': '[{"texto": "¿Funciona el agregado de preguntas?", "opciones": ["si", "no"]}, {"texto": "¿Preguntas abiertas en una encuesta?", "opciones": [  ]}]'
        }

        # Probando creacion de una encuesta
        respuesta = self.cliente.post('http://0.0.0.0:8000/encuestas/administrador/editar-encuesta/pasa-la-prueba-del-test/', request_json_encuesta)
        self.assertEquals(respuesta.status_code, 200)
        self.assertEquals(respuesta.json()['estatus'], u'ok')

        # Probando validacion de titulo para creacion de encuestas
        request_json_encuesta['titulo'] = ''
        respuesta = self.cliente.post('http://0.0.0.0:8000/encuestas/administrador/editar-encuesta/pasa-la-prueba-del-test/', request_json_encuesta)
        self.assertEquals(respuesta.status_code, 200)
        self.assertEquals(respuesta.json()['estatus'], u'error')
        self.assertEquals(respuesta.json()['error'], u'Se necesita un titulo para crear la encuesta')
        request_json_encuesta['titulo'] = 'test'

        # Probando validacion de encabezado para creacion de encuestas
        request_json_encuesta['encabezado'] = ''
        respuesta = self.cliente.post('http://0.0.0.0:8000/encuestas/administrador/editar-encuesta/pasa-la-prueba-del-test/', request_json_encuesta)
        self.assertEquals(respuesta.status_code, 200)
        self.assertEquals(respuesta.json()['estatus'], u'error')
        self.assertEquals(respuesta.json()['error'], u'Se necesita un encabezado para crear la encuesta')
        request_json_encuesta['encabezado'] = 'test'

        # Probando validacion de preguntas para creacion de encuestas
        request_json_encuesta['preguntas'] = '[]'
        respuesta = self.cliente.post('http://0.0.0.0:8000/encuestas/administrador/editar-encuesta/pasa-la-prueba-del-test/', request_json_encuesta)
        self.assertEquals(respuesta.status_code, 200)
        self.assertEquals(respuesta.json()['estatus'], u'error')
        self.assertEquals(respuesta.json()['error'], u'Se necesita al menos una pregunta para crear la encuesta')
        request_json_encuesta['preguntas'] = '[{"texto": "¿Funciona el agregado de preguntas?", "opciones": ["si", "no"]}, {"texto": "¿Preguntas abiertas en una encuesta?", "opciones": [  ]}]'

    def test_admin_listado_encuestas(self):
        """
        Test que prueba la carga correcta
        de la vista general del listado
        de encuestas creadas en la herramienta
        """
        self.login_user_test()
        # Probar que se visualiza la pagina logueado
        self.assertTrue(self.cliente.login(username='test', password='test'))
        respuesta = self.cliente.get('http://0.0.0.0:8000/encuestas/administrador/')
        self.assertEquals(respuesta.status_code, 200)

    def test_responder_encuesta(self):
        """
        Test que prueba la carga correcta
        de la vista general del listado
        de encuestas creadas en la herramienta
        """

        # Probar que se visualiza la pagina logueado
        self.assertTrue(self.cliente.login(username='test', password='test'))
        respuesta = self.cliente.get('http://0.0.0.0:8000/encuestas/responde/pasa-la-prueba-del-test/')
        self.assertEquals(respuesta.status_code, 200)

        request_respuestas = {
            'respuestas': '[{"pregunta": "¿Funciona el agregado de preguntas?", "valor": "0"}, {"pregunta": "¿Preguntas abiertas en una encuesta?", "valor": "No por supuesto que no"}]'
        }

        # Verificando escenario principal de llenado de encuesta
        respuesta = self.cliente.post('http://0.0.0.0:8000/encuestas/responde/pasa-la-prueba-del-test/', request_respuestas)
        self.assertEquals(respuesta.status_code, 200)
        self.assertEquals(respuesta.json()['estatus'], u'ok')

        # Verificando validacion de llenado completo
        request_respuestas = {
            'respuestas': '[{"pregunta": "¿Funciona el agregado de preguntas?", "valor": "0"}]'
        }

        respuesta = self.cliente.post('http://0.0.0.0:8000/encuestas/responde/pasa-la-prueba-del-test/', request_respuestas)
        self.assertEquals(respuesta.status_code, 200)
        self.assertEquals(respuesta.json()['estatus'], u'error')
        self.assertEquals(respuesta.json()['error'], u'Debe responder todas las preguntas')

        # Verificando validacion de llenado completo
        request_respuestas = {'respuestas': '[]'}

        respuesta = self.cliente.post('http://0.0.0.0:8000/encuestas/responde/pasa-la-prueba-del-test/', request_respuestas)
        self.assertEquals(respuesta.status_code, 200)
        self.assertEquals(respuesta.json()['estatus'], u'error')
        self.assertEquals(respuesta.json()['error'], u'Debe responder todas las preguntas')

        # Verificando validacion de respuesta a preguntas inexistentes
        request_respuestas = {'respuestas': '[{"pregunta": "¿Funciona el agregado de preguntas secretas?", "valor": "0"}, {"pregunta": "¿Preguntas abiertas en una encuesta?", "valor": "No por supuesto que no"}]'}

        respuesta = self.cliente.post('http://0.0.0.0:8000/encuestas/responde/pasa-la-prueba-del-test/', request_respuestas)
        self.assertEquals(respuesta.status_code, 200)
        self.assertEquals(respuesta.json()['estatus'], u'error')
        self.assertEquals(respuesta.json()['error'], u'La pregunta no existe en la encuesta')
