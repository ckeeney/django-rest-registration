import datetime

from django.conf import settings as root_settings
from django.test.signals import setting_changed
from rest_framework.settings import perform_import


DEFAULTS = {
    'USER_LOGIN_FIELDS': None,
    'USER_HIDDEN_FIELDS': (
        'is_active',
        'is_staff',
        'is_superuser',
        'user_permissions',
        'groups',
        'date_joined',
    ),
    'USER_PUBLIC_FIELDS': None,

    'USER_VERIFICATION_EMAIL_FIELD': 'email',
    'USER_VERIFICATION_FLAG_FIELD': 'is_active',

    'REGISTER_VERIFICATION_ENABLED': True,
    'REGISTER_VERIFICATION_PERIOD': datetime.timedelta(days=7),
    'REGISTER_VERIFICATION_URL': None,
    'REGISTER_VERIFICATION_EMAIL_TEMPLATES': {
        'subject':  'rest_registration/register/subject.txt',
        'body':  'rest_registration/register/body.txt',
    },

    'RESET_PASSWORD_VERIFICATION_PERIOD': datetime.timedelta(days=1),
    'RESET_PASSWORD_VERIFICATION_URL': None,
    'RESET_PASSWORD_VERIFICATION_EMAIL_TEMPLATES': {
        'subject': 'rest_registration/reset_password/subject.txt',
        'body': 'rest_registration/reset_password/body.txt',
    },

    'VERIFICATION_FROM_EMAIL': None,
    'VERIFICATION_REPLY_TO_EMAIL': None,
}

IMPORT_STRINGS = (
)


class RegistrationSettings(object):
    def __init__(self, user_settings, defaults, import_strings):
        if user_settings:
            self._user_settings = user_settings
        self.defaults = defaults
        self.import_strings = import_strings

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(root_settings, 'REST_REGISTRATION', {})
        return self._user_settings

    def reset_user_settings(self):
        if hasattr(self, '_user_settings'):
            del self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults.keys():
            raise AttributeError("Invalid registration setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        setattr(self, attr, val)
        return val


settings = RegistrationSettings(None, DEFAULTS, IMPORT_STRINGS)  # noqa


def settings_changed_handler(*args, **kwargs):
    settings.reset_user_settings()

setting_changed.connect(settings_changed_handler)
