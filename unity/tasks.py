from datetime import datetime
from celery import shared_task
from unity.models import UserEmails


@shared_task()
def send_mail_weekly():
    # Get all new email registered this month
    all_emails_this_month = UserEmails.objects.filter(cre_dt__year=datetime.now().year,
                                                      cre_dt__month=datetime.now().month).count()
    print(f'New emails this month: {all_emails_this_month}')
