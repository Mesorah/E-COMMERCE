import pytest
from django.test import TestCase
from django.urls import resolve, reverse

from staff_management import views
from utils.for_tests.base_for_setup import create_ordered_setup


@pytest.mark.test
class TestOrderedDetail(TestCase):
    def setUp(self):
        self.ordered = create_ordered_setup()
        self.client.login(username='test', password='123')

        return super().setUp()

    def test_if_staff_detail_load_the_correct_view(self):
        response = resolve(reverse('staff:ordered_detail', kwargs={
            'pk': '1'
        }))

        self.assertEqual(response.func.view_class, views.OrderedDetailView)

    def test_if_ordered_detail_load_the_correct_template(self):
        response = self.client.get(reverse('staff:ordered_detail', kwargs={
            'pk': '1'
        }))

        self.assertTemplateUsed(
            response,
            'staff_management/pages/ordered_detail.html'
        )
