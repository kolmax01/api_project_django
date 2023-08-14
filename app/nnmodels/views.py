from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import NnModels
from nnmodels import serializers


class NnModelsViewSet(viewsets.ModelViewSet):
    "basic view for nnmodels api"
    serializer_class = serializers.NnModelsDetailSerializer
    queryset = NnModels.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).\
            order_by('used_for')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.NnModelsSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
