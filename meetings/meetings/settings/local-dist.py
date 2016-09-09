"""Copy this file into local.py for local development"""


SECRET_KEY = 'CHANGEME'  # Set to large random value in your local.py
DEBUG = True
CLIENT_ID = ''
CLIENT_SECRET = ''
MAILGUN_API_KEY = ''

OSF_API_URL = ('https://staging-api.osf.io').rstrip('/') + '/'
OSF_ACCOUNTS_URL = ('https://staging-accounts.osf.io').rstrip('/') + '/'
OSF_MEETINGS_API_URL = 'http://localhost:8000'
DEFAULT_SCOPES = ['osf.full_write', ]
HUMANS_GROUP_NAME = 'OSF_USERS'
OSF_MEETINGS_API_URL = 'http://localhost:8000'
OSF_MEETINGS_HOME_URL = 'http://localhost:4200'

# Database
# POSTGRES_NAME = ''
# POSTGRES_USER = ''
# POSTGRES_PASSWORD = ''
# POSTGRES_HOST = ''
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': POSTGRES_NAME,
#         'USER': POSTGRES_USER,
#         'PASSWORD': POSTGRES_PASSWORD,
#         'HOST': POSTGRES_HOST,
#         'PORT': '',
#     }
# }
