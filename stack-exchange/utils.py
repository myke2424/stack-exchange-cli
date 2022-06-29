from markdownify import markdownify as md
from rich.markdown import Markdown


def html_to_markdown(html: str) -> Markdown:
    """ Parse html into rich markdown """
    return Markdown(md(html))
