import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DJANGO_DS_MAIN.settings')

app = Celery('DJANGO_DS_MAIN')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'compile-scss-every-hour': {
        'task': 'main.tasks.compile_scss_and_deploy_assets',
        'schedule': crontab(minute=0, hour='*'),
        'args': (1,),
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')