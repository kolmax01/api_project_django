from rest_framework import serializers
from core.models import NnModels


class NnModelsSerializer(serializers.ModelSerializer):

    class Meta:
        model = NnModels
        fields = ['id', 'title', 'used_for', 'model_size']
        read_only_fields = ['id']


class NnModelsDetailSerializer(NnModelsSerializer):

    class Meta(NnModelsSerializer.Meta):
        fields = NnModelsSerializer.Meta.fields + ['description']
