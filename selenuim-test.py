import random
import time

from fake_useragent import UserAgent
# from selenium import webdriver
from seleniumwire import webdriver

# Это тестик для проверки моих сил
randomIP = ['36.92.70.209',
            '161.202.226.194',
            '23.251.138.105',
            '42.117.2.104',
            '91.202.240.208	']
randomPorts = ['8080',
               '8123',
               '8080',
               '3128',
               '51678']
a = random.randint(0, len(randomIP))
randomip = f'{randomIP[a]}:{randomPorts[a]}'
# Словарь прокси
proxy_options = {
    'proxy': {

    }
}

# Объекткласса юзер агент
useragent = UserAgent()

# options испоьзуется для изменения параметров браузера, к примеру user-agent
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={useragent.random}')
# Прокси
print(randomip)
options.add_argument(f'--proxy-server={randomip}')

my_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
browser = webdriver.Chrome(r'C:\Users\solex\Desktop\tradebot\chromedriver.exe',
                           chrome_options=options
                           )
url = 'https://www.mirea.ru/'
try:
    browser.get(url=url)
    button = browser.find_element_by_class_name('uk-button uk-button-primary"')
except Exception as ex:
    print(ex)
finally:
    browser.close()
    browser.quit()
