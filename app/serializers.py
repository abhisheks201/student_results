from rest_framework import serializers
from .models import User, Marks


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'hall_ticket', 'gender', 'school', 'password']

    def validate_hall_ticket(self, value):
        if len(str(value)) > 10:
            raise serializers.ValidationError("Hall ticket number cannot exceed 10 digits.")
        return value
    

class MarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marks
        fields = ['user', 'telugu', 'hindi', 'english', 'maths', 'science', 'social']


        