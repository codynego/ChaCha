from rest_framework  import serializers
from .models import User, Review, Interest

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
    

class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email','phone_number', 'bio', 'interest', 'rating', 'profile_picture', 'last_seen', 'followers_count']

    def get_followers_count(self, obj):
        return obj.followers.count()
    

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user', 'reviewed_user','content', 'rating', 'created_at']
        read_only_fields = ('user','reviewed_user')

    def create(self, validated_data):
        user = self.context.get('user')
        r_user = self.context.get('reviewed_user')
        return Review.objects.create(user=user,reviewed_user=r_user, **validated_data)
    


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'profile_picture']


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['user','name']
        read_only_fields = ('user',)

    def create(self, validated_data):
        user = self.context.get('user')
        return Interest.objects.create(user=user, **validated_data)