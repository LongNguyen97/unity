from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError

from unity.models import UserEmails


def is_valid_user_mail(email):
    """
    Validate an email is valid or not.
    """
    try:
        validate_email(email)
    except ValidationError as e:
        print(f"Email validation failed: {e}")
        return False
    return True


class UserEmailRepository:
    def add_user_email(self, data):
        """
        Add new user email to DB
        """
        message, status = 'Email registered successfully!', 200
        received_mail = data.get('email')
        is_valid_email = is_valid_user_mail(received_mail.strip())

        if not is_valid_email:
            message = 'Email is invalid'
            status = 400
        else:
            try:
                UserEmails.objects.create(**{'user_mail': received_mail})
            except IntegrityError:
                message = 'Email already existed'
                status = 400

        return message, status

    def get_email_stats(self):
        all_mails = UserEmails.objects.all().order_by('-cre_dt')
        all_emails_this_month = all_mails.filter(cre_dt__year=datetime.now().year,
                                                 cre_dt__month=datetime.now().month)
        unsubscribed = all_mails.filter(status='Unsubscribed')

        return {
            'all_mails': f'{all_mails.count():,}',
            'all_emails_this_month': f'{all_emails_this_month.count():,}',
            'unsubscribed': f'{unsubscribed.count():,}',
            'display_mail': all_mails,
            'current_time': datetime.now().strftime('%B %Y')
        }
