from django.test import TestCase
from django.urls import resolve, reverse

from staff_management import views
from staff_management.forms import SupportStaffForm
from utils.for_tests.base_for_authentication import register_super_user


class TestSupportStaff(TestCase):
    def setUp(self):
        register_super_user()

        self.client.login(username='test', password='123')

        self.data = {
            'email': 'testemail@gmail.com',
            'answer': 'Answer test'
        }

        return super().setUp()

    def test_staff_support_staff_load_the_correct_view(self):
        response = resolve(reverse('staff:support_staff'))

        self.assertEqual(response.func.view_class, views.SupportStaff)

    def test_staff_support_staff_load_the_correct_template(self):
        response = self.client.get(reverse('staff:support_staff'))

        self.assertTemplateUsed(
            response,
            'staff_management/pages/support_staff.html'
        )

    def test_staff_support_staff_returns_200(self):
        response = self.client.get(reverse('staff:support_staff'))

        self.assertEqual(response.status_code, 200)

    def test_staff_support_staff_returns_302(self):
        response = self.client.post(
            reverse('staff:support_staff'),
            data=self.data
        )

        self.assertRedirects(response, reverse('staff:support_view_staff'))

    def test_support_staff_email_not_found(self):
        data = {
            'answer': 'Answer test'
        }

        response = self.client.post(
            reverse('staff:support_staff'),
            data=data
        )

        form = SupportStaffForm(data)

        self.assertIn('email', form.errors)

        self.assertEqual(response.status_code, 200)

    def test_support_staff_answer_not_found(self):
        data = {
            'email': 'testemail@gmail.com',
        }

        response = self.client.post(
            reverse('staff:support_staff'),
            data=data
        )

        form = SupportStaffForm(data)

        self.assertIn('answer', form.errors)

        self.assertEqual(response.status_code, 200)

    def test_support_staff_email_answer_not_found(self):
        data = {
            'email': 'email_not_found',
            'answer': 'answer_not_found'
        }

        response = self.client.post(
            reverse('staff:support_staff'),
            data=data
        )

        self.assertEqual(response.status_code, 200)
