# Пакет для настройки и работы с браузером.
from configparser import ConfigParser
from time import sleep
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from browser_exeptions import no_such_element
import vpn_func


def parse_settings() -> str:
    config = ConfigParser()
    config.read('config.ini')
    return config


class Browser:
    def __init__(self, headless=True):
        """
        В данном классе реализуются методы работы с браузером, в частности со Стимом:
        -авторизация
        -парсер всех вещей
        -перепродажа (not available!)
        """
        self.options = Options()
        if headless:
            self._enable_headless()
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        """
        Инициализация веб-драйвера.

        Парсятся значение PATH в config.ini. Включается возможность парсить вывод консоли разработчика для отлова
        ошибок JavaScript. Возвращается экземпляр объекта Webdriver с нужными настройками.
        """
        settings = parse_settings()
        vpn_func.start_vpn()
        dc = DesiredCapabilities.CHROME
        dc['goog:loggingPrefs'] = {'browser': 'ALL'}

        return webdriver.Chrome(executable_path=settings['Webdriver']['PATH'],
                                chrome_options=self.options, desired_capabilities=dc)

    def _enable_headless(self):
        """
        Включение headless режима. Отключение gpu в работе браузера. Настройка разрешения окна браузера.
        Опимальное разрешение 1024px в ширину, т.е. для классических мониторов и 100px в высоту для уменьшения нагрузки.
        """
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('window-size=1024,100')

    def close_browser(self):
        self.driver.close()
        self.driver.quit()

    def sign_in_steam(self):
        """
        Авторизация в Стим.
        """
        steam_link = 'https://store.steampowered.com/?l=english'

        load_dotenv()
        username = os.getenv('EMAIL')
        password = os.getenv('PASSWORD')

        self.driver.get(steam_link)
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_xpath("//*[@id='global_action_menu']/a").click()
        sleep(2)
        self.driver.find_element_by_name('username').send_keys(username)
        sleep(1)
        self.driver.find_element_by_name('password').send_keys(password)
        sleep(1)
        self.driver.find_element_by_css_selector('button[type=submit]').click()
        print('Авторизация прошла успешно!')
        sleep(2)

    @no_such_element
    def _get_item(self, item) -> tuple:
        """
        Получения значения appid и hash_name из веб элемента вещи с торговой площадки.
        """
        app_id = item.find_element_by_css_selector(
            '.market_listing_row.market_recent_listing_row.market_listing_searchresult').get_attribute('data-appid')
        hash_name = item.find_element_by_css_selector('.market_listing_row.market_recent_listing_row'
                                                      '.market_listing_searchresult').get_attribute('data-hash-name')
        return app_id, hash_name

    def get_items_on_page(self, page_num) -> list:
        """
        Получение списка кортежей с информацией о предметах на конкретной странице торговой площадки.
        В каждом кортеже лежит информация о элементе: appid и hash_name.
        """
        link = f'https://steamcommunity.com/market/search?q=#p{page_num}_popular_desc'
        self.driver.get(link)
        sleep(3)
        self.driver.implicitly_wait(5)

        items_list = self.driver.find_elements_by_css_selector('.market_listing_row_link')
        while len(items_list) != 10:
            vpn_func.switch_vpn()
            print('Длина не 10!')
            self.driver.refresh()
            items_list = self.driver.find_elements_by_css_selector('.market_listing_row_link')

        cars_list = list()
        for item in items_list:
            cars_list.append(self._get_item(item))
        return cars_list

    def get_max_page(self):
        buttons = self.driver.find_elements_by_css_selector('.market_paging_pagelink')
        return int(buttons[len(buttons) - 1].get_attribute('innerText'))
