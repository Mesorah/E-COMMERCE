import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_chrome_driver():
    options = Options()

    if os.environ.get('HEADLESS') == '1':
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
