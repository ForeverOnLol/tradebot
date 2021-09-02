from utils.logger import logging
from browser import Browser

if __name__ == '__main__':
    browser = Browser(headless=False)
    browser.sign_in_steam()
    browser.close_browser()




