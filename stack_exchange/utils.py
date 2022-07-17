import datetime
from pathlib import Path

import yaml
from markdownify import markdownify as md
from rich.markdown import Markdown


def html_to_markdown(html: str) -> Markdown:
    """Parse html string into rich markdown"""
    return Markdown(md(html))


def load_yaml_file(file_path: str) -> dict:
    """Load yaml file into dict"""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Failed to load yaml file. File path: [{path}] doesn't exist.")

    with path.open() as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


def epoch_time_to_datetime_str(timestamp: int) -> str:
    """Parse epoch unix timestamp to a datetime str"""
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
