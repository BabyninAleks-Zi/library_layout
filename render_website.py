import json
from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape


env = Environment(
    loader=FileSystemLoader("."),
    autoescape=select_autoescape(["html", "xml"]),
)


def build():
    template = env.get_template("template.html")
    with open("meta_data.json", "r", encoding="utf-8") as my_file:
        books = json.load(my_file)

    rendered_page = template.render(books=books)

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(rendered_page)


if __name__ == "__main__":
    build()

    server = Server()
    server.watch("template.html", build)
    server.watch("meta_data.json", build)
    server.serve(root=".", host="0.0.0.0", port=8000, default_filename="index.html")
