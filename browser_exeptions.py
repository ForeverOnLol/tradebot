from selenium.common import exceptions
from utils.logger import logging


def no_such_element(func):
    def wrapper(*args):
        try:
            return func(*args)
        except exceptions.NoSuchElementException:
            logging.error(msg='Ошибка. Одно из полей элемента не найдено.')
        except exceptions.ElementNotSelectableException:
            logging.error(msg='Ошибка. Станица не прогружена до конца.')
        except exceptions.StaleElementReferenceException:
            logging.error(msg='Не догружено!')

    return wrapper
