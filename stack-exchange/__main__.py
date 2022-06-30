
"""
Design patterns

- Singleton app configuration / logger
- Proxy pattern: Cache stack exchange request
- Chain of Responsibility: Log files or multiple websites
- ThreadPool for multiple site requests, can implement threadpool myself for ObjectPool pattern
- Builder potentially for building complex requests with a lot of parameters!? Idk.
- Memento or State pattern for going back and forth between question answers in interactive mode?


Code Interfaces!!!

stack_exchange = StackExchange()

stack_exchange.search(query="Reverse linked list", site="stackoverflow")

Command line interface

se will be short for stack exchange

se <query>

-q or --query

by default you should be able to search without doing -q, but if anyother kwargs used, --query is required.

se <how to reverse a linked list>

se <query> --site

se how to reverse a linked list --site="stackoverflow" 

se -i how to reverse a linked list

-i = interactive mode!

-t or --tags 

type n to see next search result in fast search.
"""

code = 'print "Hello World"'

# TUI
from rich.markdown import Markdown

from textual import events
from textual.app import App
from textual.widgets import Header, Footer, Placeholder, ScrollView


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

        async def get_markdown(markdown_str) -> None:
            readme = Markdown(markdown_str, hyperlinks=True)
            await body.update(readme)

        await self.call_later(get_markdown, 5)


# CONVERT HTML TO MARKDOWN FOR BETTER RENDERING
# USE TUI FOR FRONTEND!
# Maybe use State Pattern for interative mode?

# at least one creation pattern OR behaviour pattern!
def main():
   pass
if __name__ == "__main__":
    main()
