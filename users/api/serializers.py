from rest_framework import serializers

from users.models import CustomUser, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['level', 'exp_points', 'health_points']


    def update(self, instance, validated_data):
        instance.level = validated_data.get('level', instance.level)
        instance.exp_points = validated_data.get('exp_points', instance.exp_points)
        instance.health_points = validated_data.get('health_points', instance.health_points)
        instance.save()
        return instance


class CustomUserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'picture', 'telegram_id', 'profile']

    @staticmethod
    def get_profile(obj):
        try:
            profile = UserProfile.objects.get(user=obj)
            return UserProfileSerializer(profile).data
        except UserProfile.DoesNotExist:
            return None
