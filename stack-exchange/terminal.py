from textual import events
from textual.app import App
from textual.widgets import Header, Footer, Placeholder, ScrollView

from rich.markdown import Markdown
from .utils import html_to_markdown


class MyApp(App):
    """An example of a very simple Textual App"""

    async def on_load(self, event: events.Load) -> None:
        """Bind keys with the app loads (but before entering application mode)"""
        await self.bind("b", "view.toggle('sidebar')", "Toggle sidebar")
        await self.bind("q", "quit", "Quit")
        await self.bind("escape", "quit", "Quit")


    async def on_mount(self, event: events.Mount) -> None:
        """Create and dock the widgets."""

        # A scrollview to contain the markdown file
        body = ScrollView(gutter=1)

        # Header / footer / dock
        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")
        await self.view.dock(Placeholder(name="StackExchange Results"), edge="left", size=30, name="sidebar")

        # Dock the body in the remaining space
        await self.view.dock(body, edge="right")
        self.load_markdown(body, md)
        #
        # async def get_markdown(markdown_str) -> None:
        #     readme = Markdown(markdown_str, hyperlinks=True)
        #     await body.update(readme)
        #
        # await self.call_later(get_markdown, 5)

    async def load_markdown(self, body, md):
        await body.update(md)
