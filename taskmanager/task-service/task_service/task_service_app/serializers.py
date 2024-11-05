from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        validated_data['owner_email'] = self.context['request'].user.email
        return Task.objects.create(**validated_data)