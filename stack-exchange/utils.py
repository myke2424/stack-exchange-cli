from markdownify import markdownify as md
from rich.markdown import Markdown
from pathlib import Path
import toml


def html_to_markdown(html: str) -> Markdown:
    """Parse html into rich markdown"""
    return Markdown(md(html))


def load_toml_file(file_path: str) -> dict:
    """ Load toml file into dict """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Failed to load toml file. File path: {path} doesn't exist.")

    with path.open() as f:
        config = toml.load(f)
    return config
