import argparse
from collections import defaultdict

import pandas as pd
from datetime import datetime

from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_world_year(year: int) -> str:
    year_temp = year % 100
    if 5 <= year_temp <= 20:
        return f'{year} лет'
    year_temp = year_temp % 10
    if year_temp == 1:
        return f'{year} год'
    if 2 <= year_temp <= 4:
        return f'{year} года'
    return f'{year} лет'


def parse_argument():
    parser = argparse.ArgumentParser(
        description='Сайт магазина авторского вина "Новое русское вино"',
    )
    parser.add_argument(
        '--wine',
        default='wine_example.xlsx',
        help='Excel-файл с ассортиментом продукции',
    )
    arg = parser.parse_args()
    return arg.wine


def main():
    OPENING_DATE = '01/01/1917'
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    year_work = datetime.now()
    opening_date = datetime.strptime(OPENING_DATE, '%d/%m/%Y')
    age = year_work.year - opening_date.year
    wine_path = parse_argument()
    try:
        wines = pd.read_excel(wine_path, na_values='nan', keep_default_na=False).sort_values(by=['Категория', 'Цена']) \
            .to_dict(orient='records')
    except FileNotFoundError:
        print(f'Файл {wine_path} не найден. Проверьте имя файла и перезапустите скрипт')
        return
    wines_catalog = defaultdict(list)
    for wine in wines:
        wines_catalog[wine['Категория']].append(wine)
    rendered_page = template.render(
        year_work_world=get_world_year(age),
        data=wines_catalog,
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
