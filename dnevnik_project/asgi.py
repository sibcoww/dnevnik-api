"""
Asynchronous WSGI config for dnevnik_project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dnevnik_project.settings')
application = get_asgi_application()
