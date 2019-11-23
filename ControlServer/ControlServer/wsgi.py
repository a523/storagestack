"""
WSGI config for ControlServer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
# import asyncio
# import threading

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ControlServer.settings')

application = get_wsgi_application()

# thread_loop = asyncio.new_event_loop()
#
#
# def start_loop(loop):
#     asyncio.set_event_loop(loop)
#     loop.run_forever()
#
#
# t = threading.Thread(target=start_loop, args=(thread_loop,), daemon=True)
# t.start()
