from rest_framework import serializers as ser
from django_countries.fields import CountryField

from conferences.models import Conference


class ConferenceSerializer(ser.ModelSerializer):
    title = ser.CharField(required=True)
    city = ser.CharField()
    state = ser.CharField()
    country = CountryField() #get country_dict working later
    start = ser.DateTimeField(source='event_start', required=False)
    end = ser.DateTimeField(source='event_end', required=False)
    submissionStart = ser.DateTimeField(source='submission_start', required=False)
    submissionEnd = ser.DateTimeField(source='submission_end', required=False)
    logoUrl = ser.URLField(source='logo_url', allow_blank=True)
    description = ser.CharField(allow_blank=True)
    siteUrl = ser.URLField(source='site_url')

    # Later on add tags and sponsors back
    class Meta:
        model = Conference
        fields = ('created', 'modified', 'id', 'title', 'siteUrl', 'city',
                  'state', 'country', 'start', 'end', 'submissionStart',
                  'submissionEnd', 'logoUrl', 'description')
