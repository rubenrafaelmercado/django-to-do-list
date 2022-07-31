from rest_framework import serializers
from list_admin.models import Taks


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.IntegerField(read_only=True)
    description = serializers.CharField(required=False, allow_blank=True, max_length=300)
    comment = serializers.CharField(required=False, allow_blank=True, max_length=400)

    def create(self, validated_data):
        """
        Create and return a new `Task` instance, given the validated data.
        """
        return Task.objects.create(**validated_data)


    def update(self, instance, validated_data):
        """
        Update and return an existing `Task` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.comment = validated_data.get('comment', instance.comment)        
        instance.save()
        return instance


    