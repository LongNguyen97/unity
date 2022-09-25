import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unity.settings')

app = Celery('unity')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'send-every-monday-at-8am': {
        'task': 'unity.tasks.send_mail_weekly',
        # 08:00 AM every Monday and Wednesday UTC time
        'schedule': crontab(minute=0, hour=8, day_of_week=[1, 2]),
        'args': ()
    },

}
app.conf.timezone = 'UTC'
app.autodiscover_tasks()
