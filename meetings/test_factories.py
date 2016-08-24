import factory

from submissions.models import Submission
from approvals.models import Approval
from conferences.models import Conference
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User


class ConferenceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Conference


class ApprovalFactory(factory.DjangoModelFactory):
    class Meta:
        model = Approval


class SubmissionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Submission

    approval = factory.SubFactory(ApprovalFactory)


class SocialAccountFactory(factory.DjangoModelFactory):
    class Meta:
        model = SocialAccount


class SocialTokenFactory(factory.DjangoModelFactory):
    class Meta:
        model = SocialToken


class SocialAppFactory(factory.DjangoModelFactory):
    class Meta:
        model = SocialApp


class ResponseFactory(object):
    def __init__(self, content):
        self.data = content

    def json(self):
        return self.data


def setup_view(view, request, *args, **kwargs):
    """ Mimic as_view()"""
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


def setup_view_user(view, request, user, *args, **kwargs):
    """Mimic as_view, add user"""
    view.request = request
    view.request.user = user
    view.args = args
    view.kwargs = kwargs
    return view
