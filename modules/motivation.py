"""
Motivation Center Module
Provides inspirational quotes via ZenQuotes API
"""

from rich.console import Console
from rich.panel import Panel
from rich import box
import requests

from core.api import get_json


def get_quote(console: Console) -> None:
    """
    Fetches and displays inspirational quote from API.
    """

    console.print()
    console.print("[bold green]Getting inspiration...[/bold green]")
    console.print()

    try:
        # Returns dictionary with format: [{"q": "Quote_text", "a": "Quote_author"}]
        data = get_json("https://zenquotes.io/api/random")

        if not data or not isinstance(data, list):
            console.print("[red]Error: Unexpected API response format![/red]")
            return

        quote_data = data[0]
        quote = quote_data.get('q', '')
        author = quote_data.get('a', 'Unknown')

        if not quote:
            console.print("[red]No quote available![/red]")
            console.print()
            return

        quote_text = f'[italic]"{quote}"[/italic]\n\n[dim]— {author}[/dim]'

        panel = Panel(
            quote_text,
            title="[bold green]Daily Inspiration[/bold green]",
            border_style="green",
            box=box.DOUBLE,
            padding=(1, 3),
            expand=False
        )

        console.print()
        console.print(panel)
        console.print()

    except requests.exceptions.Timeout:
        console.print("[red]Error: Request timed out![/red]")
        console.print()
    except requests.exceptions.ConnectionError:
        console.print("[red]Error: No internet connection![/red]")
        console.print()
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print()


def run_motivation(console: Console) -> None:
    """
    Main function for Motivation Center module.
    """

    while True:
        menu_text = """[green]1.[/green] [white]Get inspirational quote[/white]
[red]B.[/red] [white]Back to main menu[/white]"""

        panel = Panel(
            menu_text,
            title="[bold green]Motivation Center[/bold green]",
            border_style="green",
            box=box.ROUNDED,
            padding=(1, 8),
            expand=False
        )

        console.print()
        console.print(panel)
        console.print()

        console.print("[white]Choose option:[/white] ", end="")
        choice = input().strip().upper()

        if choice == '1':
            get_quote(console)
        elif choice == 'B':
            break
        else:
            console.print()
            console.print("[red]Invalid choice![/red]")
            console.print()
