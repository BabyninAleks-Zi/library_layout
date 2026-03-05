import json
import os
import math
from functools import partial
from livereload import Server
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape


BOOKS_ON_PAGE = 10
BOOKS_IN_ROW = 2
TEMPLATE_PATH = "template.html"
METADATA_PATH = "meta_data.json"
PAGES_DIR = "pages"
DEFAULT_PAGE = "pages/index1.html"


def create_environment():
    return Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"]),
    )


def on_reload(env):
    template = env.get_template(TEMPLATE_PATH)
    with open(METADATA_PATH, "r", encoding="utf-8") as my_file:
        books = json.load(my_file)

    pages_count = math.ceil(len(books) / BOOKS_ON_PAGE)
    books_pages = list(chunked(books, BOOKS_ON_PAGE))
    os.makedirs(PAGES_DIR, exist_ok=True)

    for page_number, books_on_page in enumerate(books_pages, start=1):
        books_by_row = list(chunked(books_on_page, BOOKS_IN_ROW))
        rendered_page = template.render(
            books_by_row=books_by_row,
            current_page=page_number,
            pages_count=pages_count,
            page_numbers=range(1, pages_count + 1),
        )

        output_path = os.path.join(PAGES_DIR, f"index{page_number}.html")
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(rendered_page)


def main():
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"]),
    )
    reload_pages = partial(on_reload, env)

    reload_pages()

    server = Server()
    server.watch(TEMPLATE_PATH, reload_pages)
    server.watch(METADATA_PATH, reload_pages)
    server.serve(root=".", default_filename=DEFAULT_PAGE)


if __name__ == "__main__":
    main()
