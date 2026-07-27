"""
Personal Learning Dashboard - Main Application
A console app for tracking learning goals and progress
"""

from rich.console import Console
from rich.panel import Panel
from rich import box

from modules.goals import run_goals_manager
from modules.motivation import run_motivation
from modules.search import run_search


def display_welcome(console: Console) -> None:

    welcome_art = """
    ╔═══════════════════════════════════════════════╗
    ║                                               ║
    ║          PERSONAL LEARNING DASHBOARD          ║
    ║                                               ║
    ║         Track • Learn • Grow • Achieve        ║
    ║                                               ║
    ╚═══════════════════════════════════════════════╝
    """

    console.print(welcome_art, style="bold cyan")
    console.print()


def display_menu(console: Console) -> None:

    menu_text = """[bold cyan]1.[/bold cyan] [white]Goals Manager[/white] - Create and track learning goals
[bold green]2.[/bold green] [white]Motivation Center[/white] - Get inspired with quotes
[bold yellow]3.[/bold yellow] [white]Knowledge Search[/white] - Quick Wikipedia lookup
[bold red]Q.[/bold red] [white]Quit[/white] - Exit application
"""

    panel = Panel(
        menu_text,
        title="[bold white]━━━ Main Menu ━━━[/bold white]",
        border_style="white",
        box=box.ROUNDED,
        padding=(1, 5),
        expand=False
    )

    console.print(panel)
    console.print()


def main() -> None:

    console = Console()

    display_welcome(console)

    while True:
        display_menu(console)

        console.print("[bold white]Choose an option:[/bold white] ", end="")
        choice = input().strip().upper()
        console.print()

        if choice == '1':
            run_goals_manager(console)

        elif choice == '2':
            run_motivation(console)

        elif choice == '3':
            run_search(console)

        elif choice == 'Q':
            console.print("[bold green]Thanks for using Learning Dashboard![/bold green]")
            console.print("[dim]Keep learning and growing![/dim]")
            console.print()
            break

        else:
            console.print("[bold red]Invalid choice. Please try again![/bold red]")
            console.print()


if __name__ == "__main__":
    main()
