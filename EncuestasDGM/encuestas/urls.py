from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.encuestas_publico),
	url(r'p/(?P<page>[0-9])+/^$', views.encuestas_publico),
    url(r'^administrador/$', views.administrador_encuestas),
    url(r'^administrador/crear-encuesta/$', views.crear_encuesta_view),
    url(r'^administrador/editar-encuesta/(?P<slug>[-_a-zA-Z0-9]+)/$', views.editar_encuesta),
    url(r'^administrador/resultados/(?P<slug>[-_a-zA-Z0-9]+)/$', views.resultados_admin),
    url(r'^responde/(?P<slug>[-_a-zA-Z0-9]+)/$', views.responder_encuesta)
]
