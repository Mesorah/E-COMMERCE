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

        #
        price = self.browser.find_element(By.CLASS_NAME, 'buy-price').text
        self.assertEqual(price, 'R$: 150,0')

        #
        quantity = self.browser.find_element(By.ID, 'quantity')
        quantity.send_keys(2)
        quantity.send_keys(Keys.ENTER)

        #
        errors = self.browser.find_elements(By.CLASS_NAME, 'messages')

        for error in errors:
            self.assertEqual(
                error.text, 'Não temos essa quantidade em estoque!'
            )

        # self.sleep()
        # quantity.send_keys(1)
        # self.sleep()
        # quantity.send_keys(Keys.ENTER)
