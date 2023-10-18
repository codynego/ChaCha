from rest_framework  import serializers
from .models import User

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(min_length=8, write_only=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']


    def validate(self, data):
        password = data.get('password')
        confirm_password = data.pop('confirm_password', None)

        if password and password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        return User.objects.create_user(**validated_data)