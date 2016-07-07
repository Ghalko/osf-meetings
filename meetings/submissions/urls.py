from django.conf.urls import url
from submissions import views

submission_list = views.SubmissionViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
submission_detail = views.SubmissionViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    url(r'^$', submission_list, name='list'),
    url(r'^(?P<submission_id>[0-9]+)/$', submission_detail, name='detail'),
]
