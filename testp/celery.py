# DJANGO_DS_MAIN/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DJANGO_DS_MAIN.settings') # <--- IMPORTANT: Use your actual project name here

app = Celery('DJANGO_DS_MAIN') # <--- IMPORTANT: Use your actual project name here

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')