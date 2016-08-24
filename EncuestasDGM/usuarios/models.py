# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


# Create your models here.
class Token(models.Model):
    """
    Modelo de token para cambio
    de password.
    """
    token = models.CharField('token', max_length=100, db_index=True)
    user = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now=True)
    expire_date = models.DateTimeField()

    def set_temporal_email(self, email=''):
        """
        Seteo del email del usuario
        de forma temporal.
        """
        self.email = email

    def save(self):
        if not self.id:
            self.user = User.objects.get(email=self.email)
            self.expire_date = timezone.now() + timedelta(hours=1)

        super(Token, self).save()
