from django.utils.text import slugify
from .models import Encuesta, Pregunta, Respuesta


def crear_encuesta(titulo, encabezado, preguntas, publicada, abierta):
    """
    Funcion que recibe los valores 
    para crear una encuesta
    en la base de datos
    """
    # Cleaning de tipos de dato
    if type(publicada) != bool:
        publicada = True if publicada == 'true' else False

    if type(abierta) != bool:
        abierta = True if abierta == 'true' else False

    if not validar_campos_encuesta(titulo, encabezado, preguntas, publicada=publicada, abierta=abierta):
        return None

    preguntas_array_objetos = [Pregunta(texto=pregunta_elemento['texto'], opciones=pregunta_elemento.get('opciones', [])) for pregunta_elemento in preguntas]
    
    encuesta = Encuesta(titulo=titulo, encabezado=encabezado, slug=slugify(titulo), preguntas=preguntas_array_objetos, publicada=publicada, abierta=abierta)
    encuesta.save()
    return encuesta


def modificar_encuesta(id, titulo, encabezado, preguntas, publicada, abierta):
    # Cleaning de tipos de dato
    if type(publicada) != bool:
        publicada = True if publicada == 'true' else False

    if type(abierta) != bool:
        abierta = True if abierta == 'true' else False

    if not validar_campos_encuesta(titulo, encabezado, preguntas, publicada=publicada, abierta=abierta):
        return None

    encuesta = Encuesta.objects(id=id)
    
    if not encuesta.modify(titulo=titulo, encabezado=encabezado, publicada=publicada, abierta=abierta):
        return None

    preguntas_array_objetos = [Pregunta(texto=pregunta_elemento['texto'], opciones=pregunta_elemento.get('opciones', [])) for pregunta_elemento in preguntas]

    if not encuesta.modify(preguntas=preguntas_array_objetos):
        return None
    return encuesta[0]


def contestar_encuesta(encuesta, respuestas):
    if len(respuestas) == 0:
        return None

    respuestas_array_objetos = []

    for respuesta in respuestas:
        pregunta = Respuesta(pregunta=respuesta['pregunta'], valor=respuesta['valor'])
        respuestas_array_objetos.append(pregunta)

    # print(respuestas_array_objetos)
    encuesta.update(add_to_set__respuestas=respuestas_array_objetos)

    return encuesta


def validar_campos_encuesta(titulo, encabezado, preguntas, abierta=False, publicada=False, respuestas=[]):
    if not titulo.strip():
        raise Exception("Se necesita un titulo para crear la encuesta")

    if not encabezado.strip():
        raise Exception("Se necesita un encabezado para crear la encuesta")

    if len(preguntas) == 0:
        raise Exception("Se necesita al menos una pregunta para crear la encuesta")

    for pregunta in preguntas:
        validar_campos_pregunta(pregunta)

    if len(respuestas) > 0:
        for respuesta in respuestas:
            valida_campos_respuesta(respuesta)

    return True


def validar_campos_pregunta(pregunta):
    if not pregunta['texto'].strip():
        raise Exception("Se necesita un texto para crear una pregunta")


def valida_campos_respuesta(respuesta):
    if not respuesta['valor'].strip():
        raise Exception("Se necesita un valor para la respuesta")

    if not respuesta['pregunta']:
        raise Exception("Se necesita una pregunta para la respuesta")
