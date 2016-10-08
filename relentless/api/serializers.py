from rest_framework import serializers
from api.models import MyUser


class UserSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = MyUser
        fields = (
            'id',
            'email',
            'full_name',
            'mobile',
            'password',
            'is_active',
            )
        extra_kwargs = {"password":{"write_only": True}}
