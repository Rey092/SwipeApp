from django.contrib.auth import get_user_model
from django.utils.timezone import now
from celery.task import task
from celery import Task

from config import celery_app
from src.users.models import Subscription

User = get_user_model()


@task(name="deactivate_expired_subs")  # task name found! celery will do its job
def run_scheduled_jobs():
    queryset = Subscription.objects.filter(is_active=True, expiration__lt=now())
    queryset.update(is_active=False)


# @celery_app.task()
# def deactivate_expired_subscriptions():
#     queryset = Subscription.objects.filter(is_active=True, expiration__lt=now())
#     queryset.update(is_active=False)
#     print(1)
#     return queryset
#
#
# @celery_app.task()
# def dgs():
#     queryset = Subscription.objects.filter(is_active=True, expiration__lt=now())
#     queryset.update(is_active=False)
#     return 1
