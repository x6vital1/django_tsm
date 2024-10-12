from django.db import models
from django.core.exceptions import ObjectDoesNotExist

nb = dict(null=True, blank=True)

class CreateTracker(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)

class CreateUpdateTracker(CreateTracker):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class GetOrNoneManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None