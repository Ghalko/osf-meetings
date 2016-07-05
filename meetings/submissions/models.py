from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Submission(models.Model):
    node_id = models.CharField(max_length=10)
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    contributors = models.ManyToManyField(User, blank=True)
    description = models.TextField()
    conference = models.ForeignKey('conferences.Conference')
    approved = models.NullBooleanField(blank=True)

    class Meta:
        ordering = ('date_created',)

    def get_absolute_url(self):
        return reverse('conferences:submissions:submission-detail', kwargs={
            'conference_id': self.conference.pk,
            'submission_id': self.pk,
        })
