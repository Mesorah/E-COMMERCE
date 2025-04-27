import pytest
from django.test import TestCase
from django.urls import resolve, reverse

from staff_management import views
from utils.for_tests.base_for_setup import create_ordered_setup


@pytest.mark.test
class TestCompleteOrdered(TestCase):
    def setUp(self):
        self.ordered = create_ordered_setup()
        self.client.login(username='test', password='123')

        return super().setUp()

    def test_staff_complete_ordered_load_the_correct_view(self):
        response = resolve(reverse('staff:ordered_complete'))

        self.assertEqual(response.func.view_class, views.CompleteOrderedView)

    def test_complete_ordered_load_the_correct_template(self):
        response = self.client.get(reverse('staff:ordered_index'))

        self.assertTemplateUsed(
            response,
            'staff_management/pages/ordered.html'
        )

    def test_has_complete_product(self):
        self.ordered.ordered = True
        self.ordered.save()
        response = self.client.get(reverse('staff:ordered_complete'))

        self.assertIn('order-info', response.content.decode('utf-8'))

    def test_no_has_complete_product(self):
        response = self.client.get(reverse('staff:ordered_complete'))

        self.assertNotIn('order-info', response.content.decode('utf-8'))
