from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
import urlparse


class OsfMeetingsAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        try:
            refererUrl = request.environ['HTTP_REFERER']
            nextUrl = urlparse.parse_qs(
                urlparse.urlparse(refererUrl).query)['next'][0]
            return nextUrl
        except KeyError:
            return settings.OSF_MEETINGS_HOME_URL
