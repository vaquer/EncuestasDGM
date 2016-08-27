# -*- coding: utf-8 -*-
import hashlib
from datetime import datetime
from django.utils.text import slugify
from .models import Encuesta, Pregunta, Respuesta


def crear_encuesta(titulo, encabezado, preguntas, publicada, abierta):
    """
    Funcion que crea un objeto Encuesta
    en base de datos y lo regresa si
    la creacion fue exitosa.
    Return: Encuesta/None
    """
    # Cleaning de tipos de dato
    if type(publicada) != bool:
        publicada = True if publicada == 'true' or publicada == 'on' else False

    if type(abierta) != bool:
        abierta = True if abierta == 'true' or abierta == 'on' else False

    # Validacion previa a la creacion de la Encuesta en base de datos
    if not validar_campos_encuesta(titulo, encabezado, preguntas, publicada=publicada, abierta=abierta):
        return None

    # Agrupacion de las preguntas en un array de objetos Pregunta
    preguntas_array_objetos = [Pregunta(texto=pregunta_elemento['texto'], opciones=pregunta_elemento.get('opciones', [])) for pregunta_elemento in preguntas]
    
    # Creacion de la encuesta en base de datos
    slug = slugify(titulo)
    if Encuesta.objects.filter(slug__startswith=slug).count() > 0:
        slug = '{0}-{1}'.format(slug, str(Encuesta.objects.filter(slug__startswith=slug).count() + 1))
    encuesta = Encuesta(titulo=titulo, encabezado=encabezado, slug=slug, preguntas=preguntas_array_objetos, publicada=publicada, abierta=abierta)
    encuesta.save()
    return encuesta


def modificar_encuesta(encuesta, titulo, encabezado, preguntas, publicada, abierta):
    """
    Funcion que modifica un objeto Encuesta
    en base de datos y lo regresa si
    la modificacion fue exitosa.
    Return: Encuesta/None
    """
    # Conversion de tipos de datos
    if type(publicada) != bool:
        publicada = True if publicada == 'true' or publicada == 'on' else False

    if type(abierta) != bool:
        abierta = True if abierta == 'true' or abierta == 'on' else False

     # Validacion previa a la modificacion de la Encuesta en base de datos
    if not validar_campos_encuesta(titulo, encabezado, preguntas, publicada=publicada, abierta=abierta):
        return None

    # Modificacion general de la encuesta en base de datos
    if not encuesta.modify(titulo=titulo, encabezado=encabezado, publicada=publicada, abierta=abierta):
        return None

    preguntas_array_objetos = [Pregunta(texto=pregunta_elemento['texto'], opciones=pregunta_elemento.get('opciones', [])) for pregunta_elemento in preguntas]

    # Modificaciones en las preguntas de la encuesta
    if not encuesta.modify(preguntas=preguntas_array_objetos):
        return None
    return encuesta


def contestar_encuesta(encuesta, respuestas):
    """
    Funcion que agrega respuestas
    en base de datos a un objeto Encuesta
    y lo regresa si la modificacion fue exitosa.
    Return: Encuesta/None
    """

    # Debe existir minimo una respuesta
    if len(respuestas) == 0 or len(respuestas) != len(encuesta.preguntas):
        raise Exception("Debe responder todas las preguntas")

    respuestas_array_objetos = []

    # Agrupacion de objetos Respuesta en un array
    for respuesta in respuestas:
        valida_campos_respuesta(respuesta, encuesta=encuesta)
        pregunta = Respuesta(pregunta=respuesta['pregunta'], valor=respuesta['valor'], hash_respuesta=hashlib.sha224(datetime.now().strftime("%y%m%d%s")).hexdigest())
        respuestas_array_objetos.append(pregunta)

    # Responder encuesta y guardar en base de datos
    encuesta.update(add_to_set__respuestas=respuestas_array_objetos)

    return encuesta


def validar_campos_encuesta(titulo, encabezado, preguntas, abierta=False, publicada=False, respuestas=[]):
    """
    Funcion que valida la existencia
    de los parametros minimos para crear
    una Encuesta en base de datos
    Return: Bool
    """
    # Validacion de existencia de titulo
    if not titulo.strip():
        raise Exception("Se necesita un titulo para crear la encuesta")

    if not encabezado.strip():
        raise Exception("Se necesita una descripción para crear la encuesta")

    if len(preguntas) == 0:
        raise Exception("Se necesita al menos una pregunta para crear la encuesta")

    for pregunta in preguntas:
        if not validar_campos_pregunta(pregunta):
            return False

    # Se validan las respuestas si existen
    if len(respuestas) > 0:
        for respuesta in respuestas:
            if not valida_campos_respuesta(respuesta):
                return False

    return True


def validar_campos_pregunta(pregunta):
    """
    Funcion que valida la existencia
    de los parametros minimos para crear
    una Pregunta en base de datos
    Return: Bool
    """
    if not pregunta['texto'].strip():
        raise Exception("Se necesita un texto para crear una pregunta")

    return True


def valida_campos_respuesta(respuesta, encuesta=None):
    """
    Funcion que valida la existencia
    de los parametros minimos para crear
    una Respuesta en base de datos
    Return: Bool
    """
    if not str(respuesta.get('valor', '')).strip():
        raise Exception("Se necesita responder la pregunta {0}".format(respuesta.get('pregunta', '')))

    if not respuesta.get('pregunta', ''):
        raise Exception("Se necesita una pregunta para la respuesta")

    if encuesta:
        if not any([pregunta.texto == respuesta['pregunta'] for pregunta in encuesta.preguntas]):
            print pregunta.texto
            print respuesta['pregunta']
            raise Exception("La pregunta no existe en la encuesta")

    return True
