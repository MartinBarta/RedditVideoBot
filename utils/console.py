from rich.console import Console
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.text import Text

console = Console()


def print_markdown(text):
    """Vytiskne rich info zprávu. Podporuje Markdown syntax."""

    md = Padding(Markdown(text), 2)
    console.print(md)


def print_step(text):
    """Vytiskne rich info zprávu."""

    panel = Panel(Text(text, justify="left"))
    console.print(panel)


def print_substep(text, style=""):
    """Vytiskne rich info zprávu bez panellingu."""
    console.print(text, style=style)
