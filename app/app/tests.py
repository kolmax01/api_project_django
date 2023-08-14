# проверка работоспособности модуля тестов

from django.test import SimpleTestCase

from app import calc


class CalcTest(SimpleTestCase):

    def test_add_numbers(self):
        response = calc.add(5, 6)

        self.assertEqual(response, 11)

    def test_subtract_numbers(self):
        response = calc.subtract(15, 10)

        self.assertAlmostEqual(response, 5)
