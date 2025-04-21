from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.functional_tests.base import BaseFunctionalTest
from utils.for_tests.base_for_setup import create_product_setup


class HomeDetailFunctionalTest(BaseFunctionalTest):
    def test_home_detail_add_product_to_cart(self):
        product = create_product_setup()

        # User view the page
        self.browser.get(self.live_server_url + reverse(
            'home:view_page', kwargs={'slug': product.name.lower()})
        )

        # User viewed the price of the product
        price = self.browser.find_element(By.CLASS_NAME, 'buy-price').text
        self.assertEqual(price, 'R$: 150,0')

        # User tries to add 2 items to cart
        quantity = self.browser.find_element(By.ID, 'quantity')
        quantity.send_keys(2)
        quantity.send_keys(Keys.ENTER)

        # User sees error message that he does not have
        # this quantity of product in stock
        errors = self.browser.find_elements(By.CLASS_NAME, 'messages')
        self.assertIn(
            'Não temos essa quantidade em estoque!',
            [error.text for error in errors]
        )

        # User tries to add an item to the cart
        quantity = self.browser.find_element(By.ID, 'quantity')
        quantity.clear()
        quantity.send_keys(1)
        quantity.send_keys(Keys.ENTER)

        cart_count = self.browser.find_element(
            By.CLASS_NAME, 'cart-count'
        ).text

        # User sees that he has 1 product in his cart
        self.assertEqual(cart_count, '1')
