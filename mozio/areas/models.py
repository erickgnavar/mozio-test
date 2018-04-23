from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class ServiceArea(TimeStampedModel, models.Model):

    provider = models.ForeignKey('providers.Provider', on_delete=models.CASCADE)

    name = models.CharField(
        _('Name'),
        max_length=50,
    )
    price = models.DecimalField(
        _('Price'),
        max_digits=8,
        decimal_places=2,
    )

    polygon = models.PolygonField(_('Polygon'))

    class Meta:
        verbose_name = _('Service Area')
        verbose_name_plural = _('Service Areas')
        default_related_name = 'service_areas'

    def __str__(self):
        return self.name

    @property
    def owner(self):
        return self.provider
