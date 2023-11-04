from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer

User = get_user_model()


class ContractorRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'phone_number', 'inn', 'password', 'is_contractor')


class UsersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        # fields = '__all__'
        read_only_fields = ('rating',)
        exclude = ('last_login', 'is_superuser', 'is_active', 'is_staff', 'password_reset_code', 'groups', 'user_permissions', 'total_rating', 'rating_votes',)
        write_only_fields = ('password',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
    
class SetRatingSerializer(serializers.Serializer):
    rating = serializers.IntegerField()

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Неверное значение рейтинга. Выберите значение от 1 до 5.")
        return value