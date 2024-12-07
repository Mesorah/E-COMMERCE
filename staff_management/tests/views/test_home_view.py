from django.test import TestCase
from utils.for_tests.base_for_authentication import (
    register_user,
    register_super_user
)
from django.urls import reverse


class TestHomeView(TestCase):
    def setUp(self):
        register_super_user()

        return super().setUp()

    def test_user_without_permission_redirects_from_staff_index(self):
        register_user()

        self.client.login(username='Test', password='Test')

        response = self.client.get(reverse('staff:index'))

        self.assertEqual(response.status_code, 302)

    def test_user_with_permissions_accesses_staff_index_and_gets_200(self):
        self.client.login(username='test', password='123')

        response = self.client.get(reverse('staff:index'))

        self.assertEqual(response.status_code, 200)

    def test_if_home_have_the_correct_template(self):
        self.client.login(username='test', password='123')

        response = self.client.get(reverse('staff:index'))

        self.assertTemplateUsed(response, 'global/pages/base_page.html')
