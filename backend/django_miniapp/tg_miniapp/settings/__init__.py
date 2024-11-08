import os
from environs import Env

env = Env()
env.read_env()

DJANGO_ENV = env('DJANGO_ENV', default='development')

if DJANGO_ENV == 'production':
    from .production import *
else:
    from .development import *
