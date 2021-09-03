#Этот файл нужен для куки, это надо ч\тобы каждый раз не регаться на сайтах
import time

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle
from configs import mypassword,mytelephone
# Это тестик для проверки моих сил
# Словарь прокси
proxy_options = {
    'proxy': {

    }
}

# Объекткласса юзер агент
useragent = UserAgent()

# options испоьзуется для изменения параметров браузера, к примеру user-agent
my_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={my_user_agent}')

browser = webdriver.Chrome(r'C:\Users\solex\Desktop\tradebot\chromedriver.exe',
                           chrome_options=options
                           )
url = 'https://vk.com/'
try:
    browser.get(url=url)
    time.sleep(5)
    email_input = browser.find_element_by_id('index_email')
    email_input.clear()
    passoword_input = browser.find_element_by_id('index_pass')
    email_input.clear()
    email_input.send_keys(mytelephone)
    time.sleep(3)
    passoword_input.clear()
    passoword_input.send_keys(mypassword)
    time.sleep(5)
    passoword_input.send_keys(Keys.ENTER)
    #button_login = browser.find_element_by_id('index_login_button').click()
    time.sleep(20)
    pickle.dump(browser.get_cookies(), open(f'{mytelephone}_cookies','wb'))

except Exception as ex:
    print(ex)
finally:
    browser.close()
    browser.quit()
