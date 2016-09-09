from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Submission(models.Model):
    node_id = models.CharField(max_length=10)
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    contributor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='submissions_contributors'
    )
    description = models.TextField()
    conference = models.ForeignKey(
        'conferences.Conference',
        on_delete=models.CASCADE, null=True)
    approval = models.OneToOneField('approvals.Approval', null=True)
    file_id = models.CharField(max_length=100, null=True)
    file_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ('date_created',)
        permissions = (
            (
                'can_set_contributor',
                'Can set the contributor for a submission'
            ),
            ('view_submission', 'Can view submission'),
        )

    class JSONAPIMeta:
        resource_name = 'submissions'
