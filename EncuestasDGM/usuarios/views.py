# -*- coding: utf-8 -*-
import hashlib
from datetime import timedelta
from django.conf import settings
from django.http import JsonResponse, Http404
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Token


# Create your views here.
def login_view(request):
    """
    Vista de login de usuarios.
    Parametros POST: username, password
    URL: /usuarios/login/
    """

    # Redireccionar usuarios logueados
    if request.user.is_authenticated():
        return redirect('/')

    form = forms.LoginForm() if request.method != 'POST' else forms.LoginForm(request.POST)
    error = ''       

    if form.is_valid():
        username = form.cleaned_data.get('username', None)
        password = form.cleaned_data.get('password', None)

        # Autenticacion
        user = authenticate(username=username, password=password)
    
        if user is None:
            error = 'Usuario y password incorrecto'

        if user:
            if not user.is_active:
                error = 'La cuenta ha sido deshabilitada'
            # Logueo y creacion de la sesion
            login(request, user)
            return redirect('/')

    return render(request, 'usuarios/login.html', {'form': form, 'error': error})


@login_required
def logout_view(request):
    """
    Endpoint para desloguear usuarios.
    URL: /usuarios/logout/
    """
    logout(request)
    return redirect('/')


def generate_password_reset(request):
    """
    Vista que genera una solicitud de
    cambio de password.
    Parametros POST: email
    URL: /usuarios/generate_password_reset/
    """
    form = forms.TokenRenewPasswordGenerator() if request.method != 'POST' else forms.TokenRenewPasswordGenerator(request.POST)
    message = link = ''

    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email', '')
            # Se genera el hash del token en base al email y la fecha
            token = hashlib.sha224('{0}{1}'.format(timezone.now().strftime("%s"), email)).hexdigest()
            token_bd = Token(token=token)
            token_bd.set_temporal_email(email)
            token_bd.save()
            # Creacion del link de cambio de password
            link = '{0}usuarios/change_password/{1}/'.format(settings.FQDN, token)

            # Se envia por mail la url con el token
            # send_email_renew_password()
            message = 'Se ha enviado un correo con las instrucciones para reestablecer tu contraseña.'

    return render(request, 'usuarios/generate_password_reset.html', {'form': form, 'message': message, 'link': link})


def change_password(request, token=None):
    """
    Vista que sirve para cambiar password de usuario.
    Parametros URL: token
    Parametros POST: password_1, password_2
    URL: /usuarios/change_password/
    """
    if not token:
        raise Http404

    # Busqueda de token
    password_token = get_object_or_404(Token, token=token)
    if password_token.expire_date < timezone.now():
        password_token.delete()
        raise Http404

    form = forms.ChangePasswords() if request.method != 'POST' else forms.ChangePasswords(request.POST)
    message = ''

    if request.method == 'POST':
        if form.is_valid():
            user = password_token.user
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            message = 'Se ha cambiado tu password'
            # Expiracion del token
            password_token.delete()

    return render(request, 'usuarios/change_password.html', {'form': form, 'message': message})


@login_required(login_url='/usuarios/login/')
def change_user_info(request):
    """
    Vista para cambiar los datos basicos
    de una cuenta de usuario.
    Parametros POST: username, first_name, last_name, email
    URL: /usuarios/change_user_info/
    """
    user_model = User.objects.get(username=request.user)

    form = forms.ChangeInfoUser(request.POST, instance=user_model) if request.method == 'POST' else forms.ChangeInfoUser(instance=user_model)
    message = ''

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            message = 'Se guardaron los cambios exitosamente'

    return render(request, 'usuarios/change_user_info.html', {'form': form, 'message': message})
