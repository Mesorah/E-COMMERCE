from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.functional_tests.staff.base import StaffBaseFunctionalTest
from utils.for_tests.base_for_setup import create_ordered_setup


class OrderedDetailFunctionalTest(StaffBaseFunctionalTest):
    def setUp(self):
        super().setUp()

        self.super_user = self.login_user(
            reverse_url='staff:ordered_index', return_super_user=True
        )

        create_ordered_setup(qtd=11)
        self.browser.refresh()

        self.browser.get(self.live_server_url + reverse(
            'staff:ordered_detail', kwargs={'pk': '5'})
        )

    def test_ordered_detail_informations_is_correct(self):
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.TAG_NAME, 'li')
            )
        )

        product = self.browser.find_element(
            By.TAG_NAME, 'li'
        ).text

        self.assertEqual(
            product,
            'Test Product - Quantidade: 1 - Preço: R$ 150,0'
        )

        product_price = self.browser.find_element(
            By.CLASS_NAME, 'product-price'
        ).text

        self.assertEqual(product_price, 'Total:\nR$ 150,0')
