from rest_framework import serializers
from education_erp.models import EducationUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationUser
        fields = ['id', 'email', 'erp_role', 'permissions']
