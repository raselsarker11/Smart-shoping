from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email", "name", "password"]

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'],
                                       name=validated_data['name']
                                         )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    
    class Meta:
        model = User
        fields = ['email', 'password']