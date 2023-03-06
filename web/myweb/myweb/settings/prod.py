from .base import*
import os

SECRET_KEY =os.environ["DJANGO_SECRET_KEY"]
DEBUG = False
ALLOWED_HOSTS = ['localhost','146.190.99.213','*']
STATIC_ROOT=os.path.join(BASE_DIR,'statichost')



