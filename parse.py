from time import sleep

from progress.bar import IncrementalBar

from browser import Browser
from psql import Db
from vpn_func import switch_vpn


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
    link = f'https://steamcommunity.com/market/search?q=#p_popular_desc'
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
        print(list_items)
        bar.next()
        db.insert_items(list_items)
