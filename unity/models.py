from datetime import datetime

from django.db import models


class UserEmails(models.Model):
    user_mail = models.CharField(unique=True, max_length=400)
    status = models.CharField(max_length=50, default='Subscribed')
    cre_dt = models.DateTimeField(blank=True, default=datetime.now)
    upd_dt = models.DateTimeField(blank=True, default=datetime.now)

    class Meta:
        managed = True
        db_table = 'user_emails'
