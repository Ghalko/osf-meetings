from django.conf.urls import url
from submissions import views

urlpatterns = [
    url(r'^$', views.SubmissionList.as_view(), name='submission-list'),
    url(r'^(?P<submission_id>[0-9]+)/$', views.SubmissionDetail.as_view(), name='submission-detail'),
]
