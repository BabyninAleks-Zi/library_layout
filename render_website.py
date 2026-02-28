import json
from livereload import Server
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape


env = Environment(
    loader=FileSystemLoader("."),
    autoescape=select_autoescape(["html", "xml"]),
)


def on_reload():
    template = env.get_template("template.html")
    with open("meta_data.json", "r", encoding="utf-8") as my_file:
        books = json.load(my_file)

    books_by_row = list(chunked(books, 2))
    rendered_page = template.render(books_by_row=books_by_row)

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(rendered_page)


if __name__ == "__main__":
    on_reload()

    server = Server()
    server.watch("template.html", on_reload)
    server.watch("meta_data.json", on_reload)
    server.serve(root=".", default_filename="index.html")
