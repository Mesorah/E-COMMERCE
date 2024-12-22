from django.test import TestCase
from django.urls import resolve, reverse

from staff_management import views
from utils.for_tests.base_for_authentication import register_super_user
from utils.for_tests.base_for_create_itens import create_question


class TestSupportQuestionDetail(TestCase):
    def setUp(self):
        self.user = register_super_user()

        self.client.login(username='test', password='123')

        self.question = create_question(self.user)

        return super().setUp()

    def test_if_staff_support_question_detail_load_the_correct_view(self):
        response = resolve(
            reverse('staff:support_question_detail',
                    kwargs={'pk': '1'}
                    )
                )

        self.assertEqual(response.func.view_class, views.SupportQuestionDetail)

    def test_if_staff_support_question_detail_load_the_correct_template(self):
        response = self.client.get(
            reverse('staff:support_question_detail',
                    kwargs={'pk': '1'}
                    )
                )

        self.assertTemplateUsed(
            response,
            'staff_management/pages/support_question_detail.html'
        )

    def test_if_staff_support_question_detail_returns_200(self):
        response = self.client.get(
            reverse('staff:support_question_detail',
                    kwargs={'pk': '1'}
                    )
                )

        self.assertEqual(response.status_code, 200)
