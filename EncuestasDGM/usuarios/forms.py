# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import Token


def validate_email(email):
    """
    Funcion que valida le existencia
    de un email en el sistema.
    """
    try:
        user = User.objects.get(email=email)
    except:
        raise forms.ValidationError('El email no existe')


class LoginForm(forms.Form):
    """
    Formulario de Login.
    """
    username = forms.CharField(label='Usuario', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))


class TokenRenewPasswordGenerator(forms.Form):
    """
    Formulario para peticion de
    regeneracion de token.
    """
    email = forms.EmailField(validators=[validate_email])


class ChangePasswords(forms.Form):
    """
    Formulario para cambio de
    password.
    """
    password_1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirma', widget=forms.PasswordInput)  

    def clean_password_2(self):
        """
        Funcion que valida la similitud
        de las password para su cambio posterior.
        """
        if self.cleaned_data['password_1'] != self.cleaned_data['password_2']:
            raise forms.ValidationError('Las password deben coincidir')

        self.cleaned_data['new_password'] = self.cleaned_data['password_1']


class ChangeInfoUser(forms.ModelForm):
    """
    Formulario de cambio de informacion.
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
