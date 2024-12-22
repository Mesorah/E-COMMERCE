from django.test import TestCase
from django.urls import resolve, reverse

from home.models import CustomerQuestion
from staff_management import views
from utils.for_tests.base_for_authentication import register_super_user
from utils.for_tests.base_for_create_itens import create_question


class TestSupportQuestionDelete(TestCase):
    def setUp(self):
        self.user = register_super_user()

        self.client.login(username='test', password='123')

        self.question = create_question(self.user)

        return super().setUp()

    def test_if_staff_support_question_delete_load_the_correct_view(self):
        response = resolve(
            reverse('staff:support_question_delete',
                    kwargs={'pk': '1'}
                    )
                )

        self.assertEqual(response.func.view_class, views.SupportQuestionDelete)

    def test_if_staff_support_question_delete_returns_302(self):
        response = self.client.post(
            reverse('staff:support_question_delete',
                    kwargs={'pk': '1'}
                    )
                )

        self.assertEqual(response.status_code, 302)

    def test_if_staff_support_question_delete_works(self):
        questions = CustomerQuestion.objects.all()

        self.assertEqual(len(questions), 1)

        self.client.post(
            reverse('staff:support_question_delete',
                    kwargs={'pk': '1'}
                    )
                )

        questions = CustomerQuestion.objects.all()

        self.assertEqual(len(questions), 0)

    def test_if_staff_support_question_delete_is_get(self):
        response = self.client.get(
            reverse('staff:support_question_delete',
                    kwargs={'pk': '1'}
                    )
                )

        self.assertEqual(response.status_code, 404)
        # Por causa do DeleteViewMixin que tem o
        # raise no método get
