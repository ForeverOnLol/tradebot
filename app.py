from psql import Db
from utils.logger import logging
from browser import Browser
from parse import update_db_all_items

if __name__ == '__main__':
    browser = Browser(headless=True)
    db = Db()
    browser.sign_in_steam()
    update_db_all_items(db, browser)
    # browser.close_browser()




