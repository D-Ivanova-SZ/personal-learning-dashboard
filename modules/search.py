"""
Knowledge Search Module
Provides quick Wikipedia lookup functionality
"""

from rich.console import Console
from rich.panel import Panel
from rich import box
import requests
import urllib.parse


def search_topic(console: Console) -> None:
    """
    Searches for a topic on Wikipedia and displays summary.
    """
    console.print()
    console.print("[bold yellow]Knowledge Search[/bold yellow]")
    console.print()

    console.print("[white]Enter topic to search:[/white] ", end="")
    topic = input().strip()

    if not topic:
        console.print("[red]Error: Topic cannot be empty![/red]")
        return

    console.print(f"\n[yellow]Searching for '{topic}'...[/yellow]")

    try:
        topic_encoded = urllib.parse.quote(topic.replace(" ", "_"))
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic_encoded}"

        # Wikipedia requires User-Agent header for app name and contact
        headers = {
            'User-Agent': 'PersonalLearningDashboard/1.0 (contact: my_email@somesite.com)'
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 404:
            console.print(f"\n[red]Topic '{topic}' not found on Wikipedia![/red]")
            return

        response.raise_for_status()
        data = response.json()

        title = data.get('title', 'Unknown')
        extract = data.get('extract', 'No description available.')
        page_url = data.get('content_urls', {}).get('desktop', {}).get('page', '')

        content = f"[bold yellow]{title}[/bold yellow]\n\n{extract}"

        if page_url:
            content += f"\n\n[blue]Full article:[/blue] [underline]{page_url}[/underline]"

        panel = Panel(
            content,
            title="[bold yellow]Wikipedia Summary[/bold yellow]",
            border_style="yellow",
            box=box.ROUNDED,
            padding=(1, 2),
            width=70
        )

        console.print()
        console.print(panel)

    except requests.exceptions.HTTPError as e:
        if "403" in str(e):
            console.print("[red]Error 403: Wikipedia requires a proper User-Agent header![/red]")
        else:
            console.print(f"[red]HTTP Error: {e}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

    console.print()


def run_search(console: Console) -> None:
    """
    Main function for Knowledge Search module.
    """
    while True:
        menu_text = (
            "[yellow]1.[/yellow] [white]Search Wikipedia[/white]\n"
            "[red]B.[/red] [white]Back to main menu[/white]"
        )

        panel = Panel(
            menu_text,
            title="[bold yellow]Knowledge Search[/bold yellow]",
            border_style="yellow",
            box=box.ROUNDED,
            padding=(1, 3),
            width=50
        )

        console.print()
        console.print(panel)
        console.print()

        console.print("[white]Choose option:[/white] ", end="")
        choice = input().strip().upper()

        if choice == '1':
            search_topic(console)
        elif choice == 'B':
            break
        else:
            console.print("\n[red]Invalid choice![/red]\n")
