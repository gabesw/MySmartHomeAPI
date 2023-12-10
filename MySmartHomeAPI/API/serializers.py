from django.contrib.auth.models import Group, User
from rest_framework import serializers
from API.models import KitchenKeepOnSwitch


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class KitchenLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenKeepOnSwitch
        fields = ['val']

    def validate_val(self, value):
        """
        Check that the val is between 0 and 2.
        """
        if not (0 <= value <= 2):
            raise serializers.ValidationError("Value must be between 0 and 2.")
        return value