from django.conf.urls import url, include
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib import admin

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^conferences/$', 
    	views.ConferenceList.as_view(), name='conference-list'),
    url(r'^conferences/(?P<pk>[0-9]+)/$', 
    	views.ConferenceDetail, name='conference-detail'),
    url(r'^conferences/(?P<conference_id>[0-9]+)/submissions/$', 
    	views.SubmissionList.as_view(), name='submission-list'),
    url(r'^conferences/(?P<conference_id>[0-9]+)/submissions/(?P<submission_id>[0-9]+)/$', 
    	views.SubmissionDetail.as_view(), name='submission-detail'),
    url(r'^auth/', 
    	views.OsfAuthorizationUrl.as_view(), name='auth'),
    url(r'^login/', 
    	views.OsfAuthorizationCode.as_view(), name='login'),
    url(r'^admin/', 
    	admin.site.urls, name='admin'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
