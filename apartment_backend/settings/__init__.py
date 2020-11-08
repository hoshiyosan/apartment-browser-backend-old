from os import getenv as __getenv


FLASK_ENV = __getenv('FLASK_ENV', 'development')


if FLASK_ENV == 'development':
    from .development import *
elif FLASK_ENV == 'production':
    from .production import *
else:
    raise ValueError('Unkown FLASK_ENV={}'.format(FLASK_ENV))
