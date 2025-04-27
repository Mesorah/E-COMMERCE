from django.test import TestCase

from utils.for_tests.base_for_create_itens import create_category


class TestModelCategory(TestCase):
    def setUp(self):
        self.category = create_category('foods')

        return super().setUp()

    def test_category_returns_correct_name(self):
        name = 'foods'

        self.assertEqual(str(self.category), name)
