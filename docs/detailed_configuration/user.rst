User configuration
==================

The ``USER_*`` fields can be set directly in the user class (specified
by ``settings.AUTH_USER_MODEL``) without using the ``USER_`` prefix
(``EMAIL_FIELD``, etc.). These settings will override these provided in
``settings.REST_REGISTRATION``.
