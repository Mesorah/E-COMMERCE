import time

from django.test import LiveServerTestCase

from utils.browser import get_chrome_driver


class BaseFunctionalTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = get_chrome_driver()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)
