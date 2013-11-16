import os

DEBUG = True

TEST_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ''))

INSTALLED_APPS = [
    'dirty_test_bits',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SECRET_KEY = 'really-not-secret'
