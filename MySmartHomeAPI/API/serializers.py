from django.contrib.auth.models import Group, User
from rest_framework import serializers
from API.models import KitchenKeepOnSwitch, GoodMorningVariable


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'password', 'groups']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


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
        if not (0 <= value <= 3):
            raise serializers.ValidationError("Value must be between 0 and 3.")
        return value
    
class GoodMorningSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodMorningVariable
        fields = ['val']

    def validate_val(self, value):
        """
        Check that the val is between 0 and 1.
        """
        if not (0 <= value <= 1):
            raise serializers.ValidationError("Value must be between 0 and 1.")
        return value