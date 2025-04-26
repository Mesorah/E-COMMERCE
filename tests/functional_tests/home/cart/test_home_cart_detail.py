from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.functional_tests.base import BaseFunctionalTest


class StaffCartDetailFunctionalTest(BaseFunctionalTest):
    def setUp(self):
        super().setUp()

        self.get_product_in_cart()

        self.browser.get(self.live_server_url + reverse(
            'home:cart_detail')
        )

    def test_staff_cart_detail_shows_product_and_total(self):
        # View the product name
        product_name = self.browser.find_element(
            By.CLASS_NAME, 'item-name'
        ).text

        self.assertEqual(product_name, 'Product-0 x1')

        # View the final price of product
        cart_summary = self.browser.find_element(
            By.CLASS_NAME, 'cart-summary'
        )
        total_value = cart_summary.find_element(
            By.TAG_NAME, 'p'
        ).text

        self.assertEqual('Valor Total: R$ 150', total_value)

    def test_staff_cart_detail_remove_product_and_see_empty_message(self):
        # Try to remove product
        remove_product = self.browser.find_element(By.CLASS_NAME, 'remove-btn')
        remove_product.click()

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'empty-cart-message')
            )
        )

        # View te message of your empty cart
        empty_cart_message = self.browser.find_element(
            By.CLASS_NAME, 'empty-cart-message'
        ).text

        self.assertEqual(
            'Carrinho vazio: Adicione algum produto para aparecer aqui!',
            empty_cart_message
        )
