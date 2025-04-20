import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from utils.browser import get_chrome_driver

# from django.test import LiveServerTestCase


class AuthorsBaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = get_chrome_driver()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)
