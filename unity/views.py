from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView

from unity.repository.usermail_repository import UserEmailRepository


class RegisgerUserEmail(APIView):

    def post(self, request):
        """
        Return a list of all users.
        """
        user_mail_repo = UserEmailRepository()
        message, code = user_mail_repo.add_user_email(request.data)
        return Response(data=message, status=code)


class StatisticsView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_mail_repo = UserEmailRepository()
        email_stats = user_mail_repo.get_email_stats()
        context.update(email_stats)
        return context
