from django.test import TestCase
from django.urls import resolve, reverse

from home.models import Ordered
from staff_management import views
from utils.for_tests.base_for_setup import create_ordered_setup


class TestOrderedComplete(TestCase):
    def setUp(self):
        self.ordered = create_ordered_setup()
        self.client.login(username='test', password='123')

        return super().setUp()

    def test_ordered_complete_load_the_correct_view(self):
        response = resolve(reverse('staff:complete_ordered', kwargs={
            'pk': '1'
        }))

        self.assertEqual(response.func.view_class, views.OrderedCompleteView)

    def test_ordered_complete_set_true_ordered(self):
        ordered = Ordered.objects.filter(pk=1).first()

        self.assertEqual(ordered.ordered, False)

        self.client.post(reverse('staff:complete_ordered', kwargs={
            'pk': '1'
        }))

        ordered = Ordered.objects.filter(pk=1).first()

        self.assertEqual(ordered.ordered, True)
