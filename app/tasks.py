from celery import shared_task

import time

@shared_task
def debug_task() -> str:
    print('Task started: Waiting for 5 seconds...')
    time.sleep(5)
    print('Task completed')
    return 'Done'
