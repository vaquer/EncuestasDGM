from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^change_password/$', views.change_password, name='logout'),
    url(r'^generate_password_reset/$', views.generate_password_reset, name='generate_password_reset'),
    url(r'^change_password/(?P<token>[-_a-zA-Z0-9]+)/$', views.change_password, name='change_password'),
    url(r'^change_user_info/$', views.change_user_info, name='change_user_info')
]