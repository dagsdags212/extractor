import argparse


def get_cli_args():
    """Returns the namespace of CLI arguments."""
    ap = argparse.ArgumentParser(
        prog="extractor",
        description="a CLI tool for extracting article metadata from supported journals",
        epilog="@Jan Samson"
    )
    ap.add_argument("url", help="article URL")
    ap.add_argument(
        "--info", 
        help="display article info",
        action="store_true"
    )
    ap.add_argument(
        "--abstract", 
        help="display article abstract",
        action="store_true"
    )
    ap.add_argument(
        "--references", 
        help="display ALL references used in the article",
        action="store_true"
    )
    ap.add_argument(
        "--authors", 
        help="display ALL authors of the article",
        action="store_true"
    )
    ap.add_argument(
        "--download",
        help="saves article content to default download directory stored in config.toml file",
        action="store_true"
    )
    ap.add_argument(
        "--figures",
        help="saves all figures used within the article",
        action="store_true"
    )

    return ap.parse_args()
