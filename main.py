from collections import defaultdict

import pandas as pd
from datetime import datetime

from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_world_year(year: int) -> str:
    year_temp = year % 100
    if 4 <= year_temp <= 20:
        return f'{year} лет'
    year_temp = year_temp % 10
    if year_temp == 1:
        return f'{year} год'
    if 2 <= year_temp <= 4:
        return f'{year} года'
    return f'{year} лет'


def main():
    OPENING_DATE = '01/01/1921'
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    year_work = datetime.now()
    opening_date = datetime.strptime(OPENING_DATE, '%d/%m/%Y')
    age = year_work.year - opening_date.year
    wines = pd.read_excel('wine.xlsx', na_values='nan', keep_default_na=False).sort_values(by=['Категория', 'Цена']) \
        .to_dict(orient='records')
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