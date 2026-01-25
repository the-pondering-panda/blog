from jinja2 import Environment, FileSystemLoader
import json
import argparse
import os


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--post", help="Path to the post to build", type=str)
    group.add_argument("--all", help="Build everything in posts/.", action="store_true")
    parser.add_argument("--home", help="Build the homepage.", action="store_true")
    return parser.parse_args()

def get_metadata(article: str) -> dict:
    metadata_file = os.path.join(article, "metadata.json")

    with open(metadata_file, "r") as f:
        return json.load(f)

def save(html: str, path: str) -> None:
    with open(path, "w") as f:
        f.write(html)

def build_home(env: Environment) -> None:
    template = env.get_template("templates/home.html")

    posts = []
    for slug in os.listdir("posts"):
        path = os.path.join("posts", slug)
        metadata = get_metadata(path)
        posts.append({
            "date": metadata["date"],
            "url": os.path.join(path, "index.html"),
            "title": metadata["title"]
        })
        
    html = template.render(posts=posts)
    save(html, "index.html")

def build_post(env: Environment, path: str) -> None:
    template = env.get_template("templates/post.html")

    nb_path = os.path.join(path, "notebook.ipynb")
    with open(nb_path, "r") as f:
        notebook = json.load(f)

    cells = notebook["cells"]
    for cell in cells:
        # Removing empty lines and joining with tabs is purely for the aesthetics.
        source = [s for s in cell["source"] if s.strip()]
        cell["content"] = "\t".join(source)
    
    metadata = get_metadata(path)
    html = template.render(title=metadata["title"], cells=cells)

    output_file = os.path.join(path, "index.html")
    save(html, output_file)

def build_all(env: Environment) -> None:
    for slug in os.listdir("posts"):
        path = os.path.join("posts", slug)
        build_post(env, path)

def main():
    args = parse_args()
    env = Environment(trim_blocks=True, lstrip_blocks=True, loader=FileSystemLoader("."))

    if args.all:
        build_all(env)

    elif args.post:
        build_post(env, args.post)

    if args.home:
        build_home(env)

if __name__ == "__main__":
    main()
