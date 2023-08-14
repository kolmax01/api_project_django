from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import NnModels
from nnmodels.serializers import NnModelsSerializer, NnModelsDetailSerializer


NNMODELS_URL = reverse('nnmodels:nnmodels-list')


def create_nnmodel(user, **params): # noqa #тест-пример описания модели для юнит-тестов
    defaults = {
        'title': 'sample model',
        'used_for': 'text',
        'model_size': 'small',
        'description': 'sample model used for testing purposes'
    }
    defaults.update(params)

    nnmodel = NnModels.objects.create(user=user, **defaults)
    return nnmodel


def detail_url(model_id):
    return reverse('nnmodels:nnmodels-detail', args=[model_id])


def create_new_user(**params):
    return get_user_model().objects.create_user(**params)


class NnmodelsTestUnauth(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(NNMODELS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class NnmodelsTestAuth(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_new_user(
            email='test@example.com',
            password='testtesttest'
        )
        self.client.force_authenticate(self.user)

    def test_get_all_models(self):
        create_nnmodel(user=self.user)
        create_nnmodel(user=self.user)
        create_nnmodel(user=self.user)

        res = self.client.get(NNMODELS_URL)

        models = NnModels.objects.all().order_by('used_for')
        serializer = NnModelsSerializer(models, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_not_all_models_for_auth_user(self):
        "отображение только тех моделей, которые добавил конкретный юзер"

        another_user = create_new_user(
            email='another@user.com',
            password='testtesttest'
        )
        create_nnmodel(user=another_user)
        create_nnmodel(user=self.user)

        res = self.client.get(NNMODELS_URL)

        models = NnModels.objects.filter(user=self.user)
        serializer = NnModelsSerializer(models, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_detail(self):
        nnmodel = create_nnmodel(user=self.user)

        url = detail_url(nnmodel.id)
        res = self.client.get(url)

        serializer = NnModelsDetailSerializer(nnmodel)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_nnmodel(self):
        payload = {
            'title': 'sample model',
            'used_for': 'text',
            'model_size': 'small'
        }
        res = self.client.post(NNMODELS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        model = NnModels.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(model, k), v)
        self.assertEqual(model.user, self.user)

    def test_partial_update(self):
        original_param = 'text'
        model = create_nnmodel(
            user=self.user,
            title='test model 1',
            used_for=original_param
        )

        payload = {'title': 'test model 2'}
        url = detail_url(model.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        model.refresh_from_db()
        self.assertEqual(model.title, payload['title'])
        self.assertEqual(model.used_for, original_param)
        self.assertEqual(model.user, self.user)

    def test_full_update(self):
        model = create_nnmodel(
            user=self.user,
            title='test model 1',
            used_for='images',
            description='any description we want'
        )

        payload = {
            'title': 'test model 2',
            'used_for': 'text',
            'model_size': 'large',
            'description': 'another description',
        }

        url = detail_url(model.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        model.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(model, k), v)
        self.assertEqual(model.user, self.user)

    def test_error_on_update_when_user_changed(self):
        new_user = create_new_user(
            email='usern@example.com',
            password='testtesttest'
        )
        model = create_nnmodel(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(model.id)
        self.client.patch(url, payload)

        model.refresh_from_db()
        self.assertEqual(model.user, self.user)

    def test_delete_successful(self):
        model = create_nnmodel(user=self.user)
        url = detail_url(model.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(NnModels.objects.filter(id=model.id).exists())

    def test_delete_another_user_nnmodel_error(self):
        new_user = create_new_user(email='another@user.com',
                                   password='anotherpassword')
        model = create_nnmodel(user=new_user)

        url = detail_url(model.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(NnModels.objects.filter(id=model.id).exists())
