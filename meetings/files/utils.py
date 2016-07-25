from __future import unicode_literals
from django.apps import AppConfig
from meetings.utils import OsfOauth2AdapterConfig

class OsfFileStorageUrls(AppConfig):
    BASE_URL = '{}oauth2/{}'.format(OsfOauth2AdapterConfig.osf_accounts_url, '{}')
    ACCESS_TOKEN_URL = base_url.format('token')
    PROFILE_URL = '{}v2/users/me/'.format(OsfOauth2AdapterConfig.osf_api_url)
    WATERBUTLER_URL = '{}v1/resources/'.format(OsfOauth2AdapterConfig.osf_files_url)
    PROJECTS_URL = '{}project/'.format(OsfOauth2AdapterConfig.osf_staging_url)
    FILE_URL = '{}{}/providers/osfstorage'.format(self.waterbutler_url, submission_obj.node_id)
