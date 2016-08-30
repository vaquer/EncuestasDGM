import json
from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from .models import Encuesta
from .model_utils import crear_encuesta, modificar_encuesta, contestar_encuesta


# Create your views here.
@login_required(login_url='/encuestas/usuarios/login/')
def administrador_encuestas(request, page=1):
    """
    Vista del admin en datos.gob
    donde se pueden ver las encuestas
    que se han creado
    URL: /encuestas/administrador/encuestas/
    METODOS: GET
    """
    encuestas = Encuesta.objects.all().order_by('-fecha_creacion')
    pagina_encuestas = False
    if len(encuestas) > 0:
        paginador_encuestas = Paginator(encuestas, 10)

        try:
            pagina_encuestas = paginador_encuestas.page(page)
        except PageNotAnInteger:
            pagina_encuestas = paginador_encuestas.page(1)
        except EmptyPage:
            pagina_encuestas = False

    return render(request, 'encuestas/administrador/encuestas.html', {'pagina': pagina_encuestas})


@login_required(login_url='/encuestas/usuarios/login/')
def editar_encuesta(request, slug=''):
    """
    Vista del admin en datos.gob
    donde se pueden editar la encuesta
    seleccionada 
    URL: /encuestas/administrador/editar-encuesta/{slug}/
    METODOS: POST, GET
    PARAMETROS_POST: {'titulo', 'encabezado', 'abierta', 'publica', 'preguntas'}
    """
    # Buscar la encuesta en la base de datos
    try:
        encuesta = Encuesta.objects.get(slug=slug)
    except:
        raise Http404

    estatus = error = ''

    # Modificar la encuesta
    if request.method == 'POST':
        try:
            if modificar_encuesta(encuesta, request.POST.get('titulo', ''), request.POST.get('encabezado', ''), json.loads(request.POST.get('preguntas', [])), request.POST.get('publicada', False), request.POST.get('abierta', False)) is not None:
                estatus = 'ok'
        except Exception, e:
            # Capura del error para feedback
            error = e
            estatus = 'error'
        return JsonResponse({'estatus': estatus, 'error': str(error)})

    return render(request, 'encuestas/administrador/editar_encuesta.html', {'encuesta': encuesta})


@login_required(login_url='/encuestas/usuarios/login/')
def crear_encuesta_view(request):
    """
    Vista del admin en datos.gob
    donde se pueden crear una encuesta
    URL: /encuestas/administrador/crear-encuesta/
    METODOS: POST, GET
    PARAMETROS_POST: {'titulo', 'encabezado', 'abierta', 'publica', 'preguntas'}
    """
    error = estatus = ''
    # Crear la encuesta
    if request.method == 'POST':
        try:
            encuesta = crear_encuesta(request.POST.get('titulo', ''), request.POST.get('encabezado', ''), json.loads(request.POST.get('preguntas', '[]')), request.POST.get('publicada', False), request.POST.get('abierta', False))
            estatus = 'ok'
        except Exception, e:
            # Se regresan los errores de la validacion
            error = e
            estatus = 'error'
        return JsonResponse({'estatus': estatus, 'error': str(error)})

    return render(request, 'encuestas/administrador/crear_encuesta.html')


@login_required(login_url='/encuestas/usuarios/login/')
def resultados_admin(request, slug=''):
    """
    Vista del admin en datos.gob
    donde se visualizan los resultados
    de una encuesta
    URL: /encuestas/administrador/resultados/{slug}
    METODOS: GET
    """
    # Buscar la encuesta en la base de datos
    try:
        encuesta = Encuesta.objects.get(slug=slug)
    except:
        raise Http404

    estatus = error = ''


    return render(request, 'encuestas/administrador/resultados_encuesta.html', {'encuesta': encuesta})


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

    # Buscar la encuesta en la base
    try:
        encuesta = Encuesta.objects.get(slug=slug, abierta=True, publicada=True)
    except:
        raise Http404

    error = estatus = ''

    # Responder encuesta
    if request.method == 'POST':
        try:
            encuesta = contestar_encuesta(encuesta, json.loads(request.POST.get('respuestas', [])))
            estatus = 'ok'
        except Exception, e:
            estatus = 'error'
            error = e
        return JsonResponse({'error': str(error), 'estatus': estatus})

    return render(request, 'encuestas/responder.html', {'encuesta': encuesta})


def encuestas_publico(request, page=1):
    """
    Vista publica en datos.gob donde
    se listan todas las encuestas abiertas
    al publico.
    URL: /encuestas/{page}/
    METODOS: GET
    """
    encuestas = Encuesta.objects.filter(abierta=True, publicada=True).order_by('-fecha_creacion')
    paginador_encuestas = Paginator(encuestas, 10)

    pagina = paginador_encuestas.page(page)

    return render(request, 'encuestas/encuestas.html', {'encuestas': pagina, 'page_number': page})
