import os
import frontmatter as fm
import shutil
import markdown
from jinja2 import Environment, FileSystemLoader

CONTENT_DIR = "content"
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "public"
STATIC_DIR = "static"
JATS_PATH = "macc.yaml"

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
md = markdown.Markdown(extensions=["fenced_code", "tables"])

def build_page(src: str, dst: str):
    post = fm.load(src)
    site = fm.load(JATS_PATH)
    metadata = post.metadata
    site_meta = site.metadata["journal"]
    print("Site meta:", site_meta)
    content = post.content
    template_name: str | object = metadata.get("template", "base.html")
    if isinstance(template_name, str):
        template = env.get_template(template_name)

        rendered = template.render(
            content=content,
            metadata=metadata,
        )

        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "w") as f:
            _ = f.write(rendered)
    else:
        print("This failed")


def build_site():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)

    _ = shutil.copytree(STATIC_DIR, os.path.join(OUTPUT_DIR, "static"))

    for root, _, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                src = os.path.join(root, file)
                rel = os.path.relpath(src, CONTENT_DIR)
                dst = os.path.join(OUTPUT_DIR, rel.replace(".md", ".html"))
                build_page(src, dst)


if __name__ == "__main__":
    build_site()
