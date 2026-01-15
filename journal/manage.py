import argparse

from loguru import logger

from build import build_site


def initialize_parsers() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="APOK CLI")
    subparsers = parser.add_subparsers(title="build", description="Build the site", dest="command", required=True)
    _ = subparsers.add_parser("build", help="Build help")
    return parser.parse_args()  # Let argparse handle errors naturally

def main():
    args = initialize_parsers()
    if args.command == "build":
        logger.info(f"Running command: {args.command}")
        build_site()

if __name__ == "__main__":
    main()
