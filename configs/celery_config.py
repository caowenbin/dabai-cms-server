#!/usr/bin/env python
# coding: utf8
__author__ = 'ye shuo'

from datetime import timedelta

from kombu import Exchange, Queue
from celery.schedules import crontab


class CeleryConfig(object):
    BROKER_URL = "amqp://guest:guest@172.168.1.79:5672"
    CELERY_RESULT_BACKEND = None
    CELERY_IGNORE_RESULT = True
    CELERY_DEFAULT_QUEUE = "default"
    CELERY_CONCURRENCY_UD = 2
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_IMPORTS = ('tasks',)

    CELERY_DIRECT_EXCHANGE = Exchange('direct', type='direct')
    CELERY_TOPIC_EXCHANGE = Exchange('topic', type='topic')

    CELERY_QUEUES = (
        Queue('default', CELERY_DIRECT_EXCHANGE, routing_key='default'),  # 默认队列
    )

    CELERY_ROUTES = {
        'tasks.sync_express_to_kd100': {'queue': 'default'}
    },

    # CELERYBEAT_SCHEDULE = {
    #     'check_refund_status': {
    #         'task': 'tasks.check_refund_status',
    #         'schedule': timedelta(seconds=10),
    #     },
    # }