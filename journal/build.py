import os
import frontmatter as fm # pyright: ignore[stubfile]
import shutil
import markdown
from jinja2 import Environment, FileSystemLoader
from loguru import logger
import sys
import config
# Setup global vars

logger.remove()

_ = logger.add(sys.stderr, level="DEBUG")

_ = logger.add("/".join([os.getcwd(), ".logs", "apok.log"]))

CONTENT_DIR = config.CONTENT_DIR
TEMPLATE_DIR = config.TEMPLATE_DIR
OUTPUT_DIR = config.OUTPUT_DIR
STATIC_DIR = config.STATIC_DIR
SITE_CONFIGURATION_FILE = config.JATS_PATH


env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR)
)  # Setup environment with TEMPLATE_DIR
md = markdown.Markdown(extensions=["fenced_code", "tables"])

def get_most_recent_articles(articles):
    pass

def build_page(src: str, dst: str) -> bool:
    """
    Renders a template from the source file provided by `src` and puts the rendered
    template in `dst`.

    args:
      - `src`: Path to the markdown file to be rendered.
      - `dst`: Path to the rendered file.

    returns:
      - `True` if page is successfully built.
      - `False` if exception is raised.
    """

    logger.info(f"Building content {src}")
    logger.info(f"Loading frontmatter {src}")
    post = fm.load(src)

    logger.debug(f"Type of `post` {type(post)}")
    site = fm.load(SITE_CONFIGURATION_FILE)

    metadata = post.metadata
    site_meta = site.metadata
    content = post.content

    for k, v in metadata.items():
        print(k, v)

    if dst.endswith(".xml"):
        try:
            template = env.get_template("article-jats.jinja")

            rendered = template.render(content=content, metadata=metadata, site=site_meta)

            os.makedirs(os.path.dirname(dst), exist_ok=True)
            
            with open(dst, "w") as f:
                _ = f.write(rendered)
        except Exception as e:
            logger.error(e)

            return False
    
    elif dst.endswith(".typ"):
        template = env.get_template("typst-template.jinja")

        rendered = template.render(content=content, metadata=metadata, site=site_meta)

        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "w") as f:
            _ = f.write(rendered)
    else:
        template = env.get_template("article.jinja")

        rendered = template.render(content=content, metadata=metadata, site=site_meta)

        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "w") as f:
            _ = f.write(rendered)

    return True


def build_site() -> None:
    """
        Iterates over all md files in CONTENT_DIR and returns success
        if no errors.
    """
    logger.info(f"Build site as {OUTPUT_DIR}")
    failed_files: list[str] = []
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
                is_success = build_page(src, dst_html)
                if not is_success:
                    failed_files.append(src)
                is_success = build_page(src, dst_xml)
                if not is_success:
                    failed_files.append(src)
                
                is_success = build_page(src, dst_typ) # Attempt to build all index.html files
                if not is_success: # Check if rendered correctly
                    failed_files.append(src)

    if len(failed_files) > 0:
        logger.warning(f"{len(failed_files)} FAILED.")
        logger.info("Exiting with code 1.")
    else:
        logger.success(f"{len(failed_files)} files failed. The path is clear. We will meet on the fields of Armageddon.")
        logger.info("Exiting with code 0.")


if __name__ == "__main__":
    _ = build_site()

