from pathlib import Path
import sys
import tomllib
from typing import Any
from extractor.selectors import TREES
from extractor.cli import cli_args

PLATFORM = sys.platform
HOME = Path.home()
CONFIG = Path("../config.toml")
DEFAULT_ARTICLE_DIRNAME = Path("articles_extractor")
DEFAULT_FIGURES_DIRNAME = Path("figures_extractor")
DEFAULT_ARTICLE_DIRPATH = HOME / DEFAULT_ARTICLE_DIRNAME
DEFAULT_FIGURES_DIRPATH = HOME / DEFAULT_FIGURES_DIRNAME

if not CONFIG.is_file():
    with open(CONFIG, "a") as cfg_file:
        cfg_file.write("[downloads]\n")
        cfg_file.write(f"article = \"{str(DEFAULT_ARTICLE_DIRPATH)}\"\n")
        cfg_file.write(f"figures = \"{str(DEFAULT_FIGURES_DIRPATH)}\"\n")
    cfg_file.close()

with open(CONFIG, "rb") as f:
    cfg = tomllib.load(f)
f.close()


