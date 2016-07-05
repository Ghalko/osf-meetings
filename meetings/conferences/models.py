from __future__ import unicode_literals

from django.db import models
from django_countries.fields import CountryField
from django.core.urlresolvers import reverse


class Conference(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    site_url = models.URLField(blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = CountryField(blank_label='(select country)')
    event_start = models.DateTimeField(blank=True, null=True)
    event_end = models.DateTimeField(blank=True, null=True)
    submission_start = models.DateTimeField(blank=True, null=True)
    submission_end = models.DateTimeField(blank=True, null=True)
    logo_url = models.URLField(blank=True)
    description = models.TextField(blank=True, max_length=500)

    class Meta:
        ordering = ('created',)

    def get_absolute_url(self):
        return reverse('conferences:detail', kwargs={
            'pk': self.pk,
        })
