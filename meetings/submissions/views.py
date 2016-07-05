from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response

from submissions.serializers import SubmissionSerializer
from submissions.models import Submission


# List of submissions
class SubmissionList(ListCreateAPIView):
    serializer_class = SubmissionSerializer
    resource_name = 'Submission'
    encoding = 'utf-8'

    def get_queryset(self):
        conference_id = self.kwargs.get('conference_id')
        return Submission.objects.filter(conference_id=conference_id)

    def post(self, request, conference_id=None, format=None):
        serializer = SubmissionSerializer(data=request.data)
        contributors = [request.user.id]

        if serializer.is_valid():
            serializer.save(contributors=contributors)
            return Response(serializer.data)

        return Response(serializer.errors)


# Detail of a submission
class SubmissionDetail(RetrieveUpdateDestroyAPIView):
    resource_name = 'Submission'
    serializer_class = SubmissionSerializer
    lookup_url_kwarg = 'submission_id'
    lookup_field = 'pk'

    def get_queryset(self):
        conference_id = self.kwargs.get('conference_id')
        return Submission.objects.filter(conference_id=conference_id)
