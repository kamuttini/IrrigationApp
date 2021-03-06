import os

from celery import Celery
# set the default Django settings module for the 'celery' program.
import requests, json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'irrigation.settings')

app = Celery('irrigation')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.task(bind=True)
def hello_world(self):
    print('Hello world!')


@app.task(bind=True)
def relay_on(self, ip, relay, area, duration):
    
    requests.request('POST', 'http://127.0.0.1:8000/register_irrigation/C/' + str(area) + '/'+duration+'/')

    # call to relay
    server_url = 'http://' + str(ip)
    url = server_url + '/update?relay=' + str(relay) + '&state=1'
    requests.request('GET', url)


@app.task(bind=True)
def relay_off(self, ip, relay):
    # call to relay
    server_url = 'http://' + str(ip)
    url = server_url + '/update?relay=' + str(relay) + '&state=0'
    requests.request('GET', url)
