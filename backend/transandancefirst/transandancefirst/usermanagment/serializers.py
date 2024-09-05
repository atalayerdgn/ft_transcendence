from rest_framework import serializers

from transandancefirst.usermanagment.models import UserManagement


class UserManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserManagement
        fields = [
            'id',
            'username',
            'password',
            'firstName',
            'lastName',
            'email',
            'createdAt',
            'updatedAt',
        ]

