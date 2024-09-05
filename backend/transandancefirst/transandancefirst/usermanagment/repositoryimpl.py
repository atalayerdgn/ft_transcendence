from typing import Tuple, List
from uuid import UUID
from django.db import models

from transandancefirst.usermanagment.interface.repository import UserRepository
from transandancefirst.usermanagment.models import UserManagement
from transandancefirst.usermanagment.serializers import UserManagementSerializer


class UserRepositoryImpl(UserRepository):

    def get_by_id(self, id: UUID) -> Tuple[dict, str]:
        try:
            model = UserManagement.objects.filter(id=id).first()
            if model:
                serializer = UserManagementSerializer(model)
                return serializer.data, ""
            return None, "User not found"
        except Exception as e:
            return None, str(e)

    def create_user(self, user_data: dict) -> Tuple[bool, str]:
        try:
            serializer = UserManagementSerializer(data=user_data)
            if serializer.is_valid():
                serializer.save()
                return True, ""
            return False, "Invalid data"
        except Exception as e:
            return False, str(e)

    def delete_user(self, id: UUID) -> Tuple[bool, str]:
        try:
            model = UserManagement.objects.filter(id=id).first()
            if model:
                model.delete()
                return True, ""
            return False, "User not found"
        except Exception as e:
            return False, str(e)

    def get_all(self) -> List[dict]:
        try:
            models = UserManagement.objects.all()
            serializer = UserManagementSerializer(models, many=True)
            return serializer.data
        except Exception as e:
            print(str(e))
            return []

    def get_by_username(self, username: str) -> Tuple[dict, str]:
        try:
            model = UserManagement.objects.filter(username=username).first()
            if model:
                serializer = UserManagementSerializer(model)
                return serializer.data, ""
            return None, "User not found"
        except Exception as e:
            return None, str(e)

    def get_by_email(self, email: str) -> Tuple[dict, str]:
        try:
            model = UserManagement.objects.filter(email=email).first()
            if model:
                serializer = UserManagementSerializer(model)
                return serializer.data, ""
            return None, "User not found"
        except Exception as e:
            return None, str(e)