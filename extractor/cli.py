import argparse


ap = argparse.ArgumentParser(
    prog="extractor",
    description="a CLI tool for extracting article metadata from supported journals",
    epilog="@Jan Samson"
)

ap.add_argument("url", help="article URL")
ap.add_argument("--abstract", help="display article abstract", action="store_true")
ap.add_argument("--references", help="display ALL references used in the article", action="store_true")
ap.add_argument("--authors", help="display ALL authors of the article", action="store_true")
ap.add_argument("--dirpaths", help="displays the paths where articles and figures are downloaded", action="store_true")

cli_args = ap.parse_args()
