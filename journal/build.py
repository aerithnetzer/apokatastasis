import logging
import os
import frontmatter as fm
import shutil
import markdown
from jinja2 import Environment, FileSystemLoader
from loguru import logger
import sys
# Setup global vars

logger.remove()

_ = logger.add(sys.stderr, level="ERROR")

_ = logger.add("/".join([os.getcwd(), ".logs", "apok.log"]))

CONTENT_DIR = "content"
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "public"
STATIC_DIR = "static"
JATS_PATH = "apok.yaml"


env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR)
)  # Setup environment with TEMPLATE_DIR
md = markdown.Markdown(extensions=["fenced_code", "tables"])


def build_page(src: str, dst: str):
    logger.info(f"Building content {src}")
    logger.info(f"Loading frontmatter {src}")
    post = fm.load(src)

    logger.debug(f"Type of `post` {type(post)}")
    site = fm.load(JATS_PATH)

    metadata = post.metadata
    site_meta = site.metadata

    content = post.content
    template_names: str | list[str] | object = metadata.get("template", "base.html")

    if dst.endswith(".xml"):
        template = env.get_template("article-jats.xml")

        rendered = template.render(content=content, metadata=metadata, site=site_meta)

        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "w") as f:
            _ = f.write(rendered)
    if dst.endswith(".typ"):
        template = env.get_template("typst-template.typ")

        rendered = template.render(content=content, metadata=metadata, site=site_meta)

        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "w") as f:
            _ = f.write(rendered)
    else:
        template = env.get_template("article.html")

        rendered = template.render(content=content, metadata=metadata, site=site_meta)

        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "w") as f:
            _ = f.write(rendered)


def build_site():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)

    _ = shutil.copytree(STATIC_DIR, os.path.join(OUTPUT_DIR, "static"))

    for root, _, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                src = os.path.join(root, file)
                rel = os.path.relpath(src, CONTENT_DIR)
                dst_html = os.path.join(OUTPUT_DIR, rel.replace(".md", ".html"))
                dst_xml = os.path.join(OUTPUT_DIR, rel.replace(".md", ".xml"))
                dst_typ = os.path.join(OUTPUT_DIR, rel.replace(".md", ".typ"))
                build_page(src, dst_html)
                build_page(src, dst_xml)
                build_page(src, dst_typ)


if __name__ == "__main__":
    build_site()
