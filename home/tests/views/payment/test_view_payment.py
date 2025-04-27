from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from home.forms import PaymentForm
from utils.for_tests.base_for_authentication import register_user
from utils.for_tests.base_for_create_itens import create_product


class TestViewPayment(TestCase):
    def setUp(self):
        user = register_user()
        self.client.login(username='Test', password='Test')

        create_product(user)

        # Tudo daqui é falso(nem vem kk)
        self.data = {
            'first_name': 'Test First',
            'last_name': 'Test Last',
            'credit_card': '4676525956252663',
            'expiration_date': '11/27',
            'cvv': '723',
            'cardholder_name': 'Test Card Name',
            'zip_code': '86390000',
            'neighborhood': 'Test Neighborhood',
            'street_name': 'Test Street name',
            'house_number': '911'
        }

        self.form = PaymentForm(self.data)

        return super().setUp()

    def test_payment_user_not_authenticated_is_redirected_to_index(self):
        self.client.logout()

        response = self.client.post(
            reverse('home:payment'),
            data=self.data
        )

        expected_url = reverse('authors:login') + '?' + urlencode(
            {'next': reverse(
                'home:payment'
                )
             }
         )

        self.assertRedirects(response, expected_url)

    def test_payment_number_of_credit_card_is_invalid(self):
        self.data['credit_card'] = '1234567891011134'

        response = self.client.post(reverse('home:payment'), data=self.data)

        self.assertFalse(self.form.is_valid())
        self.assertIn(
            'Número de cartão de crédito inválido.',
            self.form['credit_card'].errors
        )

        self.assertEqual(response.status_code, 200)

    def test_payment_informations_is_correct_and_is_post(self):
        response = self.client.post(reverse('home:payment'), data=self.data)

        self.assertEqual(response.status_code, 302)

    def test_payment_informations_is_wrong_and_is_post(self):
        self.data['expiration_date'] = '12/12'

        response = self.client.post(reverse('home:payment'), data=self.data)

        self.assertEqual(response.status_code, 200)

    def test_payment_informations_is_correct_and_is_get(self):
        self.client.post(
            reverse('home:add_to_cart', kwargs={'pk': '1'})
        )

        response = self.client.get(reverse('home:payment'), data=self.data)

        self.assertEqual(response.status_code, 200)

    def test_payment_informations_is_correct_but_no_has_product(self):
        response = self.client.get(reverse('home:payment'), data=self.data)

        self.assertRedirects(response, reverse('home:index'))

    def test_payment_len_expiration_date_is_invalid(self):
        self.data['expiration_date'] = '1212'

        response = self.client.post(reverse('home:payment'), data=self.data)

        self.assertFalse(self.form.is_valid())
        self.assertIn(
            'Formato de data inválido. Use MM/AA ou MM/YYYY.',
            self.form['expiration_date'].errors
        )

        self.assertEqual(response.status_code, 200)

    def test_payment_mount_is_less_than_1_expiration_date(self):
        self.data['expiration_date'] = '00/27'

        response = self.client.post(reverse('home:payment'), data=self.data)

        self.assertFalse(self.form.is_valid())
        self.assertIn(
            'Mês inválido.',
            self.form['expiration_date'].errors
        )

        self.assertEqual(response.status_code, 200)

    def test_payment_mount_is_greater_than_1_expiration_date(self):
        self.data['expiration_date'] = '13/27'

        response = self.client.post(reverse('home:payment'), data=self.data)

        self.assertFalse(self.form.is_valid())
        self.assertIn(
            'Mês inválido.',
            self.form['expiration_date'].errors
        )

        self.assertEqual(response.status_code, 200)

    def test_payment_year_expiration_date_len_is_2(self):
        response = self.client.post(reverse('home:payment'), data=self.data)

        self.assertTrue(self.form.is_valid())

        self.assertEqual(response.status_code, 302)

        cleaned_data = self.form.cleaned_data

        self.assertEqual(cleaned_data['expiration_date'], '11/2027')

    def test_payment_year_expiration_date_len_is_4(self):
        self.data['expiration_date'] = '11/2027'
        response = self.client.post(reverse('home:payment'), data=self.data)

        self.assertTrue(self.form.is_valid())

        self.assertEqual(response.status_code, 302)

        cleaned_data = self.form.cleaned_data

        self.assertEqual(cleaned_data['expiration_date'], '11/2027')

    def test_payment_year_expiration_date_not_is_a_number(self):
        self.data['expiration_date'] = 'ab/cd'

        response = self.client.post(reverse('home:payment'), data=self.data)

        self.assertFalse(self.form.is_valid())

        self.assertIn(
            'Formato de data inválido. Use MM/AA ou MM/YYYY.',
            self.form['expiration_date'].errors
        )

        self.assertEqual(response.status_code, 200)

    def test_payment_zip_code_is_not_allowed(self):
        self.data['zip_code'] = '01007050'

        response = self.client.post(reverse('home:payment'), data=self.data)

        self.assertFalse(self.form.is_valid())

        self.assertIn(
            'CEP diferente de cambará.',
            self.form['zip_code'].errors
        )

        self.assertEqual(response.status_code, 200)

    def test_payment_using_sessions(self):
        self.client.post(reverse('home:add_to_cart', kwargs={'pk': '1'}))

        response = self.client.post(reverse('home:payment'), data=self.data)

        self.assertEqual(response.status_code, 302)
