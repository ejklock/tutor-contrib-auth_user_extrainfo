import re
from django import db
from django.conf import settings
from django.db import models
from localflavor.br.models import BRCPFField

# Backwards compatible settings.AUTH_USER_MODEL
USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class ExtraInfo(models.Model):
    """
    This model contains two extra fields that will be saved when a user registers.
    The form that wraps this model is in the forms.py file.
    """
    user = models.OneToOneField(USER_MODEL, null=True, related_name='user+', on_delete=models.CASCADE)
    cpf = BRCPFField(unique=True, null=True)

    def clean(self):
        self.cpf = re.sub(r'[-.]', '', self.cpf)

    def save(self, *args, **kwargs):
        self.clean()  # Ensure CPF is cleaned before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} {self.cpf}'

    class Meta:
        db_table = 'auth_user_extrainfo'
