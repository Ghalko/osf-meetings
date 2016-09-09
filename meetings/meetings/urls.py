from django.conf.urls import url, include
from api import views as apiViews
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^conferences/', include(
        'conferences.urls', namespace='conferences')),
    url(r'^approvals/', include('approvals.urls', namespace='approvals')),
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^submissions/',
        include('submissions.urls', namespace='submissions')),
    url(r'^uploads/',
        include('uploads.urls', namespace='uploads')),
    url(r'^users/me', apiViews.CurrentUserView.as_view(), name='current'),
    url(r'^users/(?P<user_id>[0-9]+)/$', apiViews.CurrentUserView.as_view(),
        name='current'),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^mail/inbound/', include('mail.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
