from celery import shared_task

@shared_task
def add(args):
    return args['x'] + args['y']
