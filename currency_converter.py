import requests
import json


def parse_data():
    link = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(link)
    with open('currency.json', 'w') as f:
        json.dump(response.json(), f, ensure_ascii=False)


def _get_currency():
    with open('currency.json', 'r') as f:
        data = json.load(f)
    cur = data['Valute']['USD']['Value']
    return cur


def convert_currency(dollars: float):
    cur = _get_currency()
    return cur * dollars
