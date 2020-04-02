from rest_framework import serializers
from api.models import PreviousProject, User, UserProfile


class PreviousProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreviousProject
        fields = [
            'id',
            'title',
            'content',
            'githubURL',
            'imageURL',
            'tags',
            'likes',
            'pub_date',
        ]

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("the length of the title should be more than 3")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('mobile',)


""" UserSerializer: Writable Nested Serializer as defined in the DRF documentation. That is, a serializer that uses 
another serializer for a particular field """


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        """By using set_password, the password is hashed and stored as a hash rather than plaintext which is a very 
        important point in terms of security. """
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.mobile = profile_data.get('mobile', profile.mobile)
        profile.save()

        return instance
