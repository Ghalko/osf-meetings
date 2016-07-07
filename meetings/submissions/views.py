from rest_framework.response import Response
from rest_framework import viewsets

from submissions.serializers import SubmissionSerializer
from submissions.models import Submission


class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    encoding = 'utf-8'
    lookup_url_kwarg = 'submission_id'
    lookup_field = 'pk'

    def get_queryset(self):
        conference_id = self.kwargs.get('conference_id')
        return Submission.objects.filter(conference_id=conference_id)

    def create(self, request, *args, **kwargs):
        serializer = SubmissionSerializer(data=request.data,
                                          context={'request': request})
        contributors = [request.user.id]

        if serializer.is_valid():
            serializer.save(contributors=contributors)
            return Response(serializer.data)

        return Response(serializer.errors)

