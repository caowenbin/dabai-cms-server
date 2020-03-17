#!/usr/bin/env python
# coding: utf8
__author__ = 'ye shuo'

import os

from libs.Manager import Manager, Command, Option

from celery.bin.beat import beat

from application import ccelery


class _CeleryCommand(Manager):
    """
    celery command
    """


CeleryCommand = _CeleryCommand()


@CeleryCommand.command
def run_worker():
    """
    run celery all queue worker
    """
    ccelery.worker_main(['worker', '--loglevel=INFO', '--concurrency=2'])


@CeleryCommand.command
def run_beat():
    """
    celery beat
    """
    beat(ccelery).execute_from_commandline(
        argv=['beat', '--loglevel=INFO', '--schedule', os.path.dirname(__file__) + '/beat.db'])


class QueueWorker(Command):
    """
    run celery specified queue worker
    """
    def get_options(self):
        return [
            Option('queue_name', metavar='QUEUE_NAME', help='queue name'),
            Option('--worker_num', metavar='WORKER_NUM', help='worker num', default=2),
        ]

    def run(self, worker_num=2, queue_name=None):
        ccelery.worker_main(
            ['worker', '--loglevel=INFO', '--queues=%s' % queue_name,
             "--hostname='%h-{}'".format(queue_name), '--concurrency=%s' % worker_num]
        )


CeleryCommand.add_command('worker', QueueWorker())
