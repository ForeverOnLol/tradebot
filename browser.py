# Пакет для настройки и работы с браузером.
import time
from configparser import ConfigParser
from time import sleep
from dotenv import load_dotenv
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

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
        steam_code = self.to_mail()
        self.driver.find_element_by_css_selector('.authcode_entry_input.authcode_placeholder').send_keys(steam_code)
        self.driver.find_element_by_css_selector('.authcode_entry_input.authcode_placeholder').send_keys(Keys.ENTER)
        time.sleep(2)
        self.driver.find_element_by_id('success_continue_btn').click()
        time.sleep(20)
    def to_mail(self):
        load_dotenv()
        mail_url = 'https://e.mail.ru/inbox/0:16307767860865543862:0/'
        mailru = os.getenv('MYLOGIN')
        steam_code = None
        pas = os.getenv('MYPAS')
        self.driver.execute_script("window.open('','_blank');")
        self.driver.switch_to_window(self.driver.window_handles[1])
        self.driver.get(mail_url)
        time.sleep(2)
        #self.driver.switch_to_window()
        login_box = self.driver.find_element_by_class_name('input-0-2-51')
        login_box.send_keys(mailru)
        login_box.send_keys(Keys.ENTER)
        time.sleep(2)
        password_box = self.driver.find_element_by_css_selector('.input-0-2-51.withIcon-0-2-52')
        password_box.send_keys(pas)
        password_box.send_keys(Keys.ENTER)
        time.sleep(5)
        self.driver.get('https://e.mail.ru/inbox/')
        time.sleep(3)
        code_letter = self.driver.find_elements_by_css_selector('.llc.js-tooltip-direction_letter-bottom.js-letter-list-item.llc_normal')[0].click()
        time.sleep(3)
        steam_code = self.driver.find_element_by_css_selector('.title-48_mr_css_attr.c-blue1_mr_css_attr.fw-b_mr_css_attr.a-center_mr_css_attr').text
        self.driver.close()
        self.driver.switch_to_window(self.driver.window_handles[0])
        return steam_code