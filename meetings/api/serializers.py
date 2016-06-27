from django.contrib.auth.models import User, Group
from api.models import Submission, Conference, Tag
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Group
		fields = ('url', 'name')

class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = ('id', 'lower',)

class SubmissionSerializer(serializers.ModelSerializer):
	conference = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name='conference-detail')
	tags = TagSerializer(many=True)
	contributors = serializers.PrimaryKeyRelatedField(many=False, queryset=Group.objects.all())
	node_id = serializers.CharField(read_only=True)
	class Meta:
		model = Submission
		fields = ('id', 'node_id', 'title', 'description', 'conference', 'tags', 'contributors')

class ConferenceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Conference
		fields = ('created', 'modified', 'id', 'title', 'website', 'city', 
			'state', 'country', 'start_date', 'end_date', 'submission_date', 'close_date', 'logo_url', 'tags', 'sponsors', 'description')
