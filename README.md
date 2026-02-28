# Сайт-каталог книг

Статический сайт-каталог книг.
Проект генерирует HTML-страницы из `meta_data.json` с помощью Jinja2 и разбивает каталог на страницы с пагинацией.

<img width="1336" height="1278" alt="image" src="https://github.com/user-attachments/assets/e29f61ec-2b2a-4091-906c-816b8aab0c81" />

## Опубликованный сайт

https://babyninaleks-zi.github.io/library_layout/

## Запуск

1. Установить зависимости:
   `pip install -r requirements.txt`
2. Сгенерировать страницы:
   `python render_website.py`
3. Открыть:
   `http://127.0.0.1:5500/`
