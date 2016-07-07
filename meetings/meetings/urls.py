from django.conf.urls import url, include
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib import admin
from rest_framework import routers

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^conferences/', include('conferences.urls', namespace='conferences')),
    url(r'^auth/', views.OsfAuthorizationUrl.as_view(), name='auth'),
    url(r'^login/', views.OsfAuthorizationCode.as_view(), name='login'),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^authenticate/', views.AuthenticateUser.as_view(), name='authenticate'),
]
