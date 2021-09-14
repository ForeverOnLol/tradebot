from time import sleep

from progress.bar import IncrementalBar
import currency_converter
from browser import Browser
from psql import Db
from vpn_func import switch_vpn
from datetime import datetime, timedelta
import json


def update_db_all_items(db: Db, browser: Browser):
    """
    Пополнение БД информацией о вещах: appid и hash_name

    Создаём таблицу. Парсим максимальную страницу. Создаём bar для информативности.
    Проходим по всем страницам, вытаскивая данные для всех элементов с данной страницы.
    Если где-то страница не догружается - vpn переключается на другой сервер.

    Список last_items получает данные со всех предметов. Нужен для того, чтобы
    сравнивать предметы с предыдущей страницы и следующей. Список list_items копирует
    данные из last_items и его значения отправляются в БД.
    Таким образом list_items дублирует значения с last_items для проверки обновления
    страницы.
    """
    db.create_tables()
    link = f'https://steamcommunity.com/market/search?appid=730#p1_popular_desc'
    browser.driver.get(link)
    max_page = browser.get_max_page()
    bar = IncrementalBar('Загрузка страниц', max=max_page)

    list_items = list()
    for i in range(1, max_page):
        last_items = browser.get_items_on_page(i)
        if last_items == list_items:
            switch_vpn()
            last_items = browser.get_items_on_page(i)
        list_items = last_items.copy()
        bar.next()
        db.insert_items(list_items)


def update_db_all_price(db: Db, browser: Browser):
    sleep(1)
    link = 'https://steamcommunity.com/market/pricehistory/?country=RU&currency=3&appid=%s&market_hash_name=%s'
    item = db.get_item_appid_name(1)[0]
    currency_converter.parse_data()
    i = 1
    print(item)
    while item:
        browser.driver.get(link % (item[1], item[2]))
        sleep(2)
        data = json.loads(browser.get_price_text())
        for row in data["prices"]:
            dt = datetime.strptime(row[0][:14], '%b %d %Y %H')
            dt = dt + timedelta(hours=3)
            price = currency_converter.convert_currency(row[1])
            sold = int(row[2])
            db.insert_prices((item[0], dt, price, sold))
            print((item[0], dt, price, sold))
        i+=1
        item = db.get_item_appid_name(i)[0]
