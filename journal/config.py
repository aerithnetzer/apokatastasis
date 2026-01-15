from loguru import logger
import sys
import os

logger.remove()

_ = logger.add(sys.stderr, level="DEBUG")

_ = logger.add("/".join([os.getcwd(), ".logs", "apok.log"]))

CONTENT_DIR = "content"
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "public"
STATIC_DIR = "static"
JATS_PATH = "apok.yaml"
