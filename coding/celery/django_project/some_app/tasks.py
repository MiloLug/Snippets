import logging

from main_app.celery import app


@app.task(name='userprogile_update_slack_profile', ignore_result=True)
def update_slack_profile(profile_id: str, **kwargs: str):
    pass
