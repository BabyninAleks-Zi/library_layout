import json
import os
import math
from livereload import Server
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape


env = Environment(
    loader=FileSystemLoader("."),
    autoescape=select_autoescape(["html", "xml"]),
)

BOOKS_ON_PAGE = 10
BOOKS_IN_ROW = 2


def on_reload():
    template = env.get_template("template.html")
    with open("meta_data.json", "r", encoding="utf-8") as my_file:
        books = json.load(my_file)

    pages_count = math.ceil(len(books) / BOOKS_ON_PAGE)
    books_pages = list(chunked(books, BOOKS_ON_PAGE))
    os.makedirs("pages", exist_ok=True)

    for page_number, books_on_page in enumerate(books_pages, start=1):
        books_by_row = list(chunked(books_on_page, BOOKS_IN_ROW))
        rendered_page = template.render(
            books_by_row=books_by_row,
            current_page=page_number,
            pages_count=pages_count,
            page_numbers=range(1, pages_count + 1),
        )

        output_path = os.path.join("pages", f"index{page_number}.html")
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(rendered_page)


if __name__ == "__main__":
    on_reload()

    server = Server()
    server.watch("template.html", on_reload)
    server.watch("meta_data.json", on_reload)
    server.serve(root=".", default_filename="pages/index1.html")
