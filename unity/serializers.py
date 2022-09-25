from rest_framework import serializers

from unity.models import UserEmails


class UserEmailSerializer(serializers.Serializer):
    class Meta:
        model = UserEmails
        fields = ['user_mail', 'status', 'cre_dt']
