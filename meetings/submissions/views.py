import json

from rest_framework.response import Response
from rest_framework import viewsets, filters

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from submissions.permissions import SubmissionPermissions

from submissions.serializers import SubmissionSerializer

from submissions.models import Submission
from approvals.models import Approval
from allauth.socialaccount.models import SocialToken
from allauth.socialaccount.models import SocialAccount

import requests
from django.conf import settings

#
#   Basic ModelViewSet functions are expanded
#   so SwaggerUI can catch the description
#


class SubmissionViewSet(viewsets.ModelViewSet):

    """ Submission Resource """

    resource_name = 'submissions'
    serializer_class = SubmissionSerializer
    lookup_url_kwarg = 'submission_id'
    lookup_field = 'pk'
    permission_classes = (SubmissionPermissions,)

    filter_backends = (
        filters.DjangoFilterBackend, filters.DjangoObjectPermissionsFilter)

    filter_fields = ('title', 'conference', 'contributor')
    queryset = Submission.objects.all()

    #  OSF's node url
    node_url = '{}v2/nodes/'.format(settings.OSF_API_URL)

    def retrieve(self, request, *args, **kwargs):
        """Returns a single Submission item"""
        return super(SubmissionViewSet, self).retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Partial update a Submission """
        return super(SubmissionViewSet, self).partial_update(
            request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Delete a Submission"""
        return super(SubmissionViewSet, self).destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        node = {
            'data': {
                'attributes': {
                    'category': 'project',
                    'description': serializer.validated_data['description'],
                    'title': serializer.validated_data['title'],
                    'public': True
                },
                'type': 'nodes'
            }
        }
        osf_token = SocialToken.objects.get(
            account=SocialAccount.objects.get(uid=self.request.user.username)
        )
        response = requests.post(
            self.node_url,
            data=json.dumps(node),
            headers={
                'Authorization': 'Bearer {}'.format(osf_token),
                'Content-Type': 'application/json; charset=UTF-8'
            }
        )
        osf_response = response.json()
        serializer.save(
            contributor=self.request.user,
            approval=Approval.objects.create(),
            node_id=osf_response['data']['id']
        )

    @method_decorator(login_required)
    def create(self, request, *args, **kwargs):
        """Create a submission"""
        return super(SubmissionViewSet, self).create(request, *args, **kwargs)

    @method_decorator(login_required)
    def update(self, request, *args, **kwargs):
        """Updates a single Submission item"""
        current_user = request.user.username
        account = SocialAccount.objects.get(uid=current_user)
        osf_token = SocialToken.objects.get(account=account)

        update_node = {
            'data': {
                'attributes': {
                    'category': 'project',
                    'title': request.data['title']
                },
                'type': 'nodes',
                'id': request.data['node_id']
            }
        }

        # Update OSF's node
        response = requests.put(
            '{}{}/'.format(self.node_url, request.data['node_id']),
            data=json.dumps(update_node),
            headers={
                'Authorization': 'Bearer {}'.format(osf_token),
                'Content-Type': 'application/json; charset=UTF-8'
            }
        )

        if (response.status_code == 200):
            return super(SubmissionViewSet, self).update(request, args, kwargs)
        return Response(response.text, status=response.status_code)
