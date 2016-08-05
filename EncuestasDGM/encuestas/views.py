from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Encuesta
from .model_utils import crear_encuesta, modificar_encuesta, contestar_encuesta


# Create your views here.
@login_required(login_url='')
def administrador_encuestas(request, page=1):
    """
    Vista del admin en datos.gob
    donde se pueden ver las encuestas
    que se han creado
    URL: /encuestas/administrador/encuestas/
    METODOS: GET
    """
    pass


@login_required(login_url='')
def editar_encuesta(request, slug=''):
    """
    Vista del admin en datos.gob
    donde se pueden editar la encuesta
    seleccionada 
    URL: /encuestas/administrador/editar-encuesta/{slug}/
    METODOS: POST, GET
    PARAMETROS_POST: {'titulo', 'encabezado', 'abierta', 'publica', 'preguntas'}
    """
    pass


def responder_encuesta(request, slug=''):
    """
    Vista publica en datos.gob donde
    se responde la encuesta solicitada
    si esta publicada y abierta al publico
    URL: /encuestas/responde/{slug}/
    METODOS: POST, GET
    PARAMETROS_POST: respuestas = [{'pregunta', 'valor'}]
    """
    if not slug.strip():
        raise Http404

    try:
        encuesta = Encuesta.objects.get(slug=slug, abierta=True, publicada=True)
    except:
        raise Http404

    errores, estatus = ([], '')

    if request.method == 'POST':
        if not request.POST.get('respuestas', []):
            raise Http404
        if contestar_encuesta(encuesta.id, request.POST.get('respuestas')):
            estatus = 'ok'

    return render(request, 'template.html', {'encuesta': encuesta, 'errores': errores})