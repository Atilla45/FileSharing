from celery import shared_task

@shared_task
def export_excel():
    print('ise dusdu')
    print('dayandi')
    return True