# Пакет для настройки и работы с браузером.
from configparser import ConfigParser
from time import sleep
from dotenv import load_dotenv
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def parse_settings() -> str:
    config = ConfigParser()
    config.read('config.ini')
    return config


class Browser:
    def __init__(self, headless=True):
        self.options = Options()
        if headless:
            self._enable_headless()
        self.driver = self._initialize_driver()

    def _enable_headless(self):
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')

    def _initialize_driver(self):
        settings = parse_settings()
        if settings['Webdriver']['BROWSER'].lower() == 'chrome':
            return webdriver.Chrome(executable_path=settings['Webdriver']['PATH'],
                                    chrome_options=self.options)
        else:
            return webdriver.Firefox(executable_path=settings['Webdriver']['PATH'],
                                     firefox_options=self.options)

    def close_browser(self):
        self.driver.close()
        self.driver.quit()


    def sign_in_steam(self):
        steam_link = 'https://store.steampowered.com/?l=english'
        load_dotenv()
        username = os.getenv('EMAIL')
        password = os.getenv('PASSWORD')

        self.driver.get(steam_link)
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_class_name('global_action_link').click()
        sleep(2)

        self.driver.find_element_by_name('username').send_keys(username)
        sleep(1)

        self.driver.find_element_by_name('password').send_keys(password)
        sleep(1)

        self.driver.find_element_by_css_selector('button[type=submit]').click()
        sleep(2)


