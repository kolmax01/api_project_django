from core import models

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        email = 'test@test.com'
        password = '123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalization(self):
        #
        # TODO: добавить дополнительные сэмплы в сэмпл емэйл
        #
        sample_emails = [
            ['test0@TEST.com', 'test0@test.com'],
            ['test1@Test.com', 'test1@test.com'],
            ['TEST2@TEST.COM', 'TEST2@test.com'],
            ['test3@test.COM', 'test3@test.com']
        ]

        for email_1, email_true in sample_emails:
            user = get_user_model().objects.create_user(email_1, '123test123')
            self.assertEqual(user.email, email_true)

    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', '123test123')

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@test.com',
            '123test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_model_description_successful(self):
        user = get_user_model().objects.create_user(
            'test@test.com',
            '123test123'
        )
        nn_model = models.NnModels.objects.create(
            user=user,
            title='Test neural net',
            used_for='text/tables/images',
            model_size='small/medium/big',
            description='test test test test'
        )

        self.assertEqual(str(nn_model), nn_model.title)
