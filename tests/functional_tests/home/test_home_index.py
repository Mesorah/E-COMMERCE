from selenium.webdriver.common.by import By

from tests.functional_tests.base import BaseFunctionalTest


class HomeIndexFunctionalTest(BaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Produtos Disponíveis', body.text)
