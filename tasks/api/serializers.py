from rest_framework import serializers
from tasks.models import Tasks
from users.api.serializers import CustomUserSerializer, UserProfileSerializer
from users.models import UserProfile, CustomUser
from tasks.reminders import send_reminders, send_created_notification


class TasksSerializer(serializers.ModelSerializer):
    difficulty = serializers.CharField()
    deadline = serializers.DateTimeField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Tasks
        fields = ['id', 'title', 'description', 'difficulty', 'completed', 'deadline', 'user', 'created_at',
                  'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'user']

    def to_internal_value(self, data):
        data = data.copy()
        difficulty_mapping = dict(Tasks.DIFFICULTY_CHOICES)
        reverse_difficulty_mapping = {v.lower(): k for k, v in difficulty_mapping.items()}

        difficulty_value = data.get('difficulty', '').lower()

        # Проверяем, является ли значение числом
        if difficulty_value.isdigit():
            difficulty_value = int(difficulty_value)
            if difficulty_value not in difficulty_mapping:
                raise serializers.ValidationError({"difficulty": "Invalid difficulty value."})
            data['difficulty'] = difficulty_value
        else:
            # Проверяем, является ли значение человекочитаемой строкой
            difficulty_code = reverse_difficulty_mapping.get(difficulty_value)
            if difficulty_code is None:
                raise serializers.ValidationError({"difficulty": "Difficulty must be 'easy', 'medium', or 'hard'."})
            data['difficulty'] = difficulty_code

        return super().to_internal_value(data)

    @staticmethod
    def get_user_profile(obj):
        try:
            profile = UserProfile.objects.get(user=obj.user)
            return UserProfileSerializer(profile).data
        except UserProfile.DoesNotExist:
            return None

    @staticmethod
    def get_user(obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'telegram_id': obj.user.telegram_id,
            'picture': obj.user.picture,
        }
