import secrets

import pycountry
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class Provider(TimeStampedModel):

    name = models.CharField(
        _('Name'),
        max_length=50,
    )
    email = models.CharField(
        _('Email'),
        max_length=255,
        unique=True,
    )
    phone_number = models.CharField(
        _('Phone number'),
        max_length=20,
        validators=[
            RegexValidator(r'^\+?\d{1,15}$', _('Invalid phone number')),
        ],
    )
    language = models.CharField(
        _('Language'),
        max_length=10,
        choices=settings.LANGUAGES,
    )
    currency = models.CharField(
        _('Currency'),
        max_length=3,
        choices=list(map(lambda x: (x.alpha_3, x.name), pycountry.currencies)),
    )

    # Used for authentication
    token = models.CharField(max_length=64, default=secrets.token_hex, editable=False)

    class Meta:
        verbose_name = _('Provider')
        verbose_name_plural = _('Providers')
        default_related_name = 'providers'

    def __str__(self):
        return self.name

    def generate_token(self):
        self.token = secrets.token_hex()
        self.save()

    @property
    def owner(self):
        return self
