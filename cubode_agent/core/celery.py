# myproject/celery.py

from __future__ import absolute_import, unicode_literals
from celery import Celery


app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
