from rest_framework import serializers
from .models import BlockType, Project, BlockInstance

class BlockTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockType
        fields = '__all__'

class BlockInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockInstance
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    blocks = BlockInstanceSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'created_by', 'created_at', 'blocks']

    def create(self, validated_data):
        blocks_data = validated_data.pop('blocks')
        project = Project.objects.create(**validated_data)
        for block_data in blocks_data:
            BlockInstance.objects.create(project=project, **block_data)
        return project
