from rest_framework import serializers as ser

from submissions.models import Submission
from conferences.models import Conference

from api.serializers import UserSerializer


class SubmissionSerializer(ser.HyperlinkedModelSerializer):
    conference = ser.HyperlinkedRelatedField(view_name='conferences:detail', queryset=Conference.objects.all())
    contributors = UserSerializer(many=True)
    node_id = ser.CharField(read_only=True)

    def create(self, validated_data):
        # look up contributors by ID
        contributors = validated_data['contributors']
        title = validated_data['title']
        description = validated_data['description']
        conference = validated_data['conference']
        submission = Submission.objects.create(title=title, description=description, conference=conference, approved=False)
        for contributor in contributors:
                submission.contributors.add(contributor)
        return submission

    class Meta:
        model = Submission
        fields = ('id', 'node_id', 'title', 'description', 'conference',
                  'contributors')
