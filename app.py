from psql import Db
from utils.logger import logging
from browser import Browser
from parse import update_db_all_items, update_db_all_price

if __name__ == '__main__':
    browser = Browser(headless=False)
    db = Db()
    browser.sign_in_steam()
    # update_db_all_items(db, browser)
    update_db_all_price(db, browser)
    # browser.close_browser()




