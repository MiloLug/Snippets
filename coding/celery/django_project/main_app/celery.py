import os
from celery import Celery, shared_task
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main_app.settings")
app = Celery("main_app")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.on_after_configure.connect
def add_periodic(**kwargs):
    app.add_periodic_task(10.0, scan_tasks, name='exec every 10s')
    app.add_periodic_task(2.0, updates_applying_tasks, name='exec every 2s')


@shared_task
def scan_tasks(*args):
    app.send_task('userprofile_scan_sirens')


@shared_task
def updates_applying_tasks(*args):
    app.send_task('userprofile_apply_updates')
