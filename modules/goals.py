"""
Goals Manager Module
Handles CRUD operations for learning goals and study sessions
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from typing import Optional
from datetime import datetime, date
import time

from core.file_manager import load_data, save_data


# HELPER FUNCTIONS #

def generate_id(prefix: str) -> str:
    """
    Generates unique ID based on current timestamp.
    """
    return f"{prefix}_{int(time.time())}"


def calculate_progress(goal: dict, sessions: list) -> float:
    """
    Calculates progress percentage for a goal based on its sessions.
    Returns progress percentage (0-100)
    """

    if goal['target_hours'] == 0:
        return 0

    # Calculate total hours from sessions for this goal
    total_hours = 0
    for session in sessions:
        if session['goal_id'] == goal['id']:
            total_hours += session['duration_minutes'] / 60

    # Calculate percentage, but max 100%
    return min((total_hours / goal['target_hours']) * 100, 100)


def get_goal_hours(goal_id: str, sessions: list) -> float:
    """
    Gets total hours logged for a specific goal.
    """

    total_minutes = 0
    for session in sessions:
        if session['goal_id'] == goal_id:
            total_minutes += session['duration_minutes']

    return total_minutes / 60


def days_until_deadline(goal: dict) -> int:
    """
    Calculates days remaining until deadline.
    Returns number of days remaining (0 if overdue)
    """

    deadline = date.fromisoformat(goal['deadline'])
    today = date.today()
    delta = deadline - today
    return max(delta.days, 0)  # Return 0 if negative


def find_goal_by_id(goal_id: str, goals: list) -> Optional[dict]:
    """
    Finds a goal by its ID in list of goal dictionaries
    Returns goal dictionary if found, None otherwise
    """

    for goal in goals:
        if goal['id'] == goal_id:
            return goal
    return None


def calculate_streak(sessions: list) -> int:
    """
    Calculates current study streak (consecutive days with sessions).
    Returns number of consecutive days with study sessions
    """

    if not sessions:
        return 0

    # Extract unique dates from sessions
    session_dates = set()
    for session in sessions:
        session_date = datetime.fromisoformat(session['date']).date()
        session_dates.add(session_date)

    # Start from today and count backwards
    today = date.today()
    streak = 0
    current_date = today

    # Check consecutive days going backwards
    while current_date in session_dates:
        streak += 1
        # Move to previous day
        current_date = date.fromordinal(current_date.toordinal() - 1)

    return streak


# DISPLAY FUNCTIONS #

def display_goals_table(goals: list, sessions: list, console: Console) -> None:
    """
    Displays all goals in a formatted Rich table.
    """

    if not goals:
        console.print("[yellow]No goals yet. Create your first goal![/yellow]")
        console.print()
        return

    table = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(0, 1)
    )

    table.add_column("#", style="dim", width=3)
    table.add_column("Title", style="white", no_wrap=False)
    table.add_column("Category", style="cyan")
    table.add_column("Progress", style="green", width=15)
    table.add_column("Hours", style="yellow")
    table.add_column("Deadline", style="magenta")
    table.add_column("Status", style="bold")

    for id_num, goal in enumerate(goals, 1):
        progress = calculate_progress(goal, sessions)
        hours = get_goal_hours(goal['id'], sessions)
        days_left = days_until_deadline(goal)

        status_map = {
            'active': 'Active',
            'completed': 'Done',
            'paused': 'Paused'
        }
        status_display = status_map.get(goal['status'], goal['status'])

        # Progress bar (10 characters)
        bar_length = 10
        filled = int((progress / 100) * bar_length)
        bar = '█' * filled + '░' * (bar_length - filled)
        progress_display = f"{bar} {progress:.0f}%"

        # Hours display
        hours_display = f"{hours:.1f}/{goal['target_hours']}"

        # Deadline display
        if days_left > 0:
            deadline_display = f"{days_left}d left"
        else:
            deadline_display = "Overdue"

        table.add_row(
            str(id_num),
            goal['title'],
            goal['category'],
            progress_display,
            hours_display,
            deadline_display,
            status_display
        )

    panel = Panel(
        table,
        title="[bold cyan]Your Learning Goals[/bold cyan]",
        border_style="cyan",
        padding=(1, 4),
        expand=False
    )

    console.print(panel)
    console.print()


def display_sessions_table(sessions: list, goals: list, console: Console) -> None:
    """
    Displays recent study sessions in a table.
    """

    if not sessions:
        console.print("[yellow]No study sessions logged yet![/yellow]")
        console.print()
        return

    # Sort sessions by date (most recent first)
    sorted_sessions = sorted(
        sessions,
        key=lambda s: s['date'],
        reverse=True
    )

    # Show only last 15 sessions
    recent_sessions = sorted_sessions[:15]

    table = Table(
        show_header=True,
        header_style="bold green",
        border_style="green",
        box=box.ROUNDED,
        padding=(0, 1)
    )

    table.add_column("Date", style="cyan")
    table.add_column("Goal", style="white")
    table.add_column("Topic", style="yellow")
    table.add_column("Duration", style="green")

    for session in recent_sessions:
        # Format date
        session_date = datetime.fromisoformat(session['date'])
        date_formatted = session_date.strftime("%Y-%m-%d %H:%M")

        # Get goal title
        goal = find_goal_by_id(session['goal_id'], goals)
        goal_title = goal['title'] if goal else "Unknown"

        # Format duration
        hours = session['duration_minutes'] / 60
        duration_str = f"{hours:.1f}h"

        table.add_row(
            date_formatted,
            goal_title,
            session['topic'],
            duration_str
        )

    panel = Panel(
        table,
        title="[bold green]Recent Study Sessions[/bold green]",
        border_style="green",
        padding=(1, 5),
        expand=False
    )

    console.print(panel)

    if len(sessions) > 15:
        console.print(f"[dim]Showing 15 most recent of {len(sessions)} total sessions[/dim]")

    console.print()


# CRUD OPERATIONS #

def create_goal(console: Console) -> None:
    """
    Creates a new learning goal through interactive prompts.
    """

    console.print("[bold cyan]Create New Learning Goal[/bold cyan]")
    console.print()

    console.print("[white]Goal title:[/white] ", end="")
    title = input().strip()
    if not title:
        console.print("[red]Error: Title cannot be empty![/red]")
        console.print()
        return

    console.print("[white]Description:[/white] ", end="")
    description = input().strip()

    console.print("[white]Category (e.g., Programming, Language, Math):[/white] ", end="")
    category = input().strip() or "General"

    console.print("[white]Target hours:[/white] ", end="")
    try:
        target_hours = int(input().strip())
        if target_hours <= 0:
            raise ValueError
    except ValueError:
        console.print("[red]Error: Please enter a valid positive number![/red]")
        console.print()
        return

    console.print("[white]Deadline (YYYY-MM-DD):[/white] ", end="")
    deadline_str = input().strip()
    try:
        deadline = date.fromisoformat(deadline_str)
        if deadline < date.today():
            console.print("[yellow]Warning: Deadline is in the past![/yellow]")
    except ValueError:
        console.print("[red]Error: Invalid date format! Use YYYY-MM-DD[/red]")
        console.print()
        return

    # Create goal dictionary
    goal = {
        'id': generate_id('goal'),
        'title': title,
        'description': description,
        'category': category,
        'target_hours': target_hours,
        'deadline': deadline.isoformat(),
        'status': 'active',
        'created_at': datetime.now().isoformat()
    }

    # Load data, then add the goal and save
    data = load_data()
    data['goals'].append(goal)

    if save_data(data):
        console.print()
        console.print("[bold green]Goal created successfully![/bold green]")
    else:
        console.print("[bold red]Failed to save goal![/bold red]")

    console.print()


def view_goals(console: Console) -> None:
    """
    Displays all goals with their progress.
    """

    data = load_data()
    goals = data.get('goals', [])
    sessions = data.get('sessions', [])

    if not goals:
        console.print()
        console.print("[yellow]No goals yet. Create your first goal![/yellow]")
        console.print()
        return

    console.print()
    console.print("[bold cyan]Your Learning Goals[/bold cyan]")
    console.print()

    display_goals_table(goals, sessions, console)

    console.print()
    console.print("[dim]Press Enter to continue...[/dim]", end="")
    input()


def log_study_session(console: Console) -> None:
    """
    Logs a new study session for a goal.
    Updates progress and auto-completes goal if target is reached.
    """

    data = load_data()
    goals = data.get('goals', [])
    sessions = data.get('sessions', [])

    if not goals:
        console.print()
        console.print("[yellow]No goals available. Create a goal first![/yellow]")
        console.print()
        return

    console.print()
    console.print("[bold green]Log Study Session[/bold green]")
    console.print()

    # Show goals to choose from
    display_goals_table(goals, sessions, console)

    console.print("[white]Select goal number:[/white] ", end="")
    try:
        goal_id = int(input().strip()) - 1
        if goal_id < 0 or goal_id >= len(goals):
            raise ValueError
        goal = goals[goal_id]
    except ValueError:
        console.print()
        console.print("[red]Invalid goal number selection![/red]")
        console.print()
        return

    # Get session details
    console.print()
    console.print(f"[cyan]Logging session for: {goal['title']}[/cyan]")
    console.print()

    console.print("[white]Duration (minutes):[/white] ", end="")
    try:
        duration = int(input().strip())
        if duration <= 0:
            raise ValueError
    except ValueError:
        console.print()
        console.print("[red]Invalid duration![/red]")
        console.print()
        return

    console.print("[white]Topic/What did you learn:[/white] ", end="")
    topic = input().strip()

    if not topic:
        console.print()
        console.print("[red]Topic cannot be empty![/red]")
        console.print()
        return

    console.print("[white]Notes (optional, press Enter to skip):[/white] ", end="")
    notes = input().strip()

    # Create session
    session = {
        'id': generate_id('session'),
        'goal_id': goal['id'],
        'date': datetime.now().isoformat(),
        'duration_minutes': duration,
        'topic': topic,
        'notes': notes
    }

    sessions.append(session)

    # Check if goal is completed
    progress = calculate_progress(goal, sessions)

    if progress >= 100 and goal['status'] != 'completed':
        goal['status'] = 'completed'
        console.print()
        console.print("[bold green]Congratulations! You completed this goal![/bold green]")

    # Save data
    data['sessions'] = sessions
    data['goals'] = goals

    if save_data(data):
        console.print()
        console.print("[green]Session logged successfully![/green]")
        console.print(f"[dim]Added {duration} minutes to '{goal['title']}'[/dim]")
        console.print()
    else:
        console.print()
        console.print("[red]Failed to save session![/red]")
        console.print()


def view_sessions(console: Console) -> None:
    """
    Displays recent study sessions.
    """

    data = load_data()
    goals = data.get('goals', [])
    sessions = data.get('sessions', [])

    if not sessions:
        console.print("[yellow]No study sessions logged yet![/yellow]")
        console.print("[dim]Use 'Log study session' to start tracking![/dim]")
        console.print()
        return

    display_sessions_table(sessions, goals, console)

    # Calculate and show streak
    streak = calculate_streak(sessions)
    if streak > 0:
        fire_emoji = "🔥" * min(streak, 5)  # Max 5 fire emojis
        console.print(
            f"[bold yellow]Current streak: {streak} {'day' if streak == 1 else 'days'} {fire_emoji}[/bold yellow]")
        console.print()

    console.print("[dim]Press Enter to continue...[/dim]", end="")
    input()


def delete_goal(console: Console) -> None:
    """
    Deletes a goal and all associated sessions.
    """
    data = load_data()
    goals = data.get('goals', [])
    sessions = data.get('sessions', [])

    if not goals:
        console.print()
        console.print("[yellow]No goals to delete![/yellow]")
        console.print()
        return

    console.print()
    console.print("[bold red]Delete Goal[/bold red]")
    console.print()

    # Show available goals
    display_goals_table(goals, sessions, console)

    console.print()
    console.print("[white]Enter Goal number to delete:[/white] ", end="")

    try:
        goal_id = int(input().strip()) - 1
        if goal_id < 0 or goal_id >= len(goals):
            raise ValueError
        goal = goals[goal_id]
    except ValueError:
        console.print()
        console.print("[red]Invalid goal number selection![/red]")
        console.print()
        return

    # Confirm deletion
    console.print()
    console.print(f"[bold red]Are you sure you want to delete '{goal['title']}'?[/bold red]")
    console.print("[dim]This will also delete all associated sessions.[/dim]")
    console.print()
    console.print("[white]Type 'yes' to confirm:[/white] ", end="")
    confirmation = input().strip().lower()

    if confirmation != 'yes':
        console.print()
        console.print("[yellow]Deletion cancelled![/yellow]")
        console.print()
        return

    # Delete goal
    goals = [g for g in goals if g['id'] != goal['id']]

    # Delete all associated sessions
    sessions = [s for s in sessions if s['goal_id'] != goal['id']]

    # Save data
    data['goals'] = goals
    data['sessions'] = sessions

    if save_data(data):
        console.print()
        console.print(f"[green]Goal '{goal['title']}' and associated sessions are deleted successfully![/green]")
        console.print()
    else:
        console.print()
        console.print("[red]Failed to delete goal![/red]")
        console.print()


# MAIN MODULE FUNCTION #

def run_goals_manager(console: Console) -> None:
    """
    Main function for Goals Manager module.
    Displays submenu and handles user choices.
    """

    while True:
        menu_text = """[cyan]1.[/cyan] [white]Create new goal[/white]
[cyan]2.[/cyan] [white]View all goals[/white]
[cyan]3.[/cyan] [white]Log study session[/white] - Track your study time
[cyan]4.[/cyan] [white]View sessions history[/white]
[cyan]5.[/cyan] [white]Delete goal[/white]
[red]B.[/red] [white]Back to main menu[/white]"""

        panel = Panel(
            menu_text,
            title="[bold cyan]Goals Manager[/bold cyan]",
            border_style="cyan",
            box=box.ROUNDED,
            padding=(1, 8),
            expand=False
        )

        console.print()
        console.print(panel)
        console.print()

        console.print("[white]Choose option:[/white] ", end="")
        choice = input().strip().upper()
        console.print()

        if choice == '1':
            create_goal(console)
        elif choice == '2':
            view_goals(console)
        elif choice == '3':
            log_study_session(console)
        elif choice == '4':
            view_sessions(console)
        elif choice == '5':
            delete_goal(console)
        elif choice == 'B':
            break
        else:
            console.print("[red]Invalid choice. Please try again![/red]")
            console.print()
