from django.test import TestCase
from django.urls import resolve, reverse

from staff_management import views
from utils.for_tests.base_for_setup import create_ordered_setup


class TestOrderedIndex(TestCase):
    def setUp(self):
        self.ordered = create_ordered_setup()

        return super().setUp()

    def test_if_staff_index_load_the_correct_view(self):
        self.client.login(username='test', password='123')
        response = resolve(reverse('staff:ordered_index'))

        self.assertEqual(response.func.view_class, views.OrderedIndexView)

    def test_if_ordered_index_load_the_correct_template(self):
        self.client.login(username='test', password='123')

        response = self.client.get(reverse('staff:ordered_index'))

        self.assertTemplateUsed(
            response,
            'staff_management/pages/ordered.html'
        )
