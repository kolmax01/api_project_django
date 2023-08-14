from django.urls import (path,
                         include)
from rest_framework.routers import DefaultRouter

from nnmodels import views


router = DefaultRouter()
router.register('nnmodels', views.NnModelsViewSet)

app_name = 'nnmodels'

urlpatterns = [
    path('', include(router.urls)),
]
