from django.urls import reverse
from selenium.webdriver.common.by import By

from tests.functional_tests.base import BaseFunctionalTest
from utils.for_tests.base_for_setup import create_product_setup


class CartDetailFunctionalTest(BaseFunctionalTest):
    def setUp(self):
        super().setUp()

        product = create_product_setup()

        self.browser.get(self.live_server_url + reverse(
            'home:view_page', kwargs={'slug': product.name.lower()})
        )

        form = self.browser.find_element(By.CLASS_NAME, 'buy-form')
        form.submit()

        self.browser.get(self.live_server_url + reverse(
            'home:cart_detail')
        )

    def test_cart_detail_can_see_product_name_and_total_price_in_cart(self):
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

    def test_cart_detail_can_remove_product_and_see_empty_cart_message(self):
        # Try to remove product
        remove_product = self.browser.find_element(By.CLASS_NAME, 'remove-btn')
        remove_product.click()

        # View te message of your empty cart
        empty_cart_message = self.browser.find_element(
            By.CLASS_NAME, 'empty-cart-message'
        ).text

        self.assertEqual(
            'Carrinho vazio: Adicione algum produto para aparecer aqui!',
            empty_cart_message
        )
