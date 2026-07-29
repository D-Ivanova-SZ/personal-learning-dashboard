# 📚 Personal Learning Dashboard

A modular Python console application for managing learning goals, tracking study sessions, visualizing progress through automated aggregation, progress analytics, study streak calculation, JSON persistence and REST API integrations.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Rich](https://img.shields.io/badge/UI-Rich-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Status](https://img.shields.io/badge/Status-Complete-success)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Screenshots](#screenshots)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Data Model](#data-model)
- [Key Algorithms](#key-algorithms)
- [Installation](#installation)
- [Usage](#usage)
- [Error Handling](#error-handling)
- [Future Development](#future-development)
- [License](#license)

---

## Overview

**Personal Learning Dashboard** addresses a common challenge for self-learners: tracking progress across multiple learning goals in a structured, motivating way. Instead of relying on scattered notes or spreadsheets, this application provides a centralized console-based tool with automated progress calculation, consistency tracking, and quick access to external knowledge resources.

The project was built with an emphasis on **clean architecture**, **data integrity**, and **algorithmic problem-solving** — going beyond basic CRUD operations to implement custom logic for progress aggregation and streak calculation.

**Target users:** students, self-learners, and professionals pursuing structured skill development.

---

## Features

| Feature | Description |
|---|---|
| 🎯 **Goal Management** | Full CRUD operations for learning goals (title, category, target hours, deadline) |
| 📝 **Session Logging** | Record study sessions with duration, topic, and notes |
| 📊 **Progress Tracking** | Progress percentage calculated dynamically from logged sessions |
| 🔥 **Streak Counter** | Tracks consecutive days of study activity per goal |
| ✅ **Auto-Completion** | Goals automatically marked complete when target hours are reached |
| 💡 **Motivation Center** | Fetches inspirational quotes via the Quotable API |
| 🔍 **Knowledge Search** | Quick topic lookups via the Wikipedia REST API |
| 🗑️ **Cascade Delete** | Deleting a goal safely removes all associated sessions |

---

## Screenshots

[Welcome Screen](screenshots/welcome_screen.png) |
[Main Menu](screenshots/main_menu.png) |
[Goals Manager](screenshots/goals_manager.png) |
[View All Goals](screenshots/view_all_goals.png) |
[Log Study Session](screenshots/log_study_session.png) |
[View Session History](screenshots/view_session_history.png) |
[Knowledge Search](screenshots/knowledge_search.png)

---

## Tech Stack

**Language & Environment**
- Python 3.9+
- Developed in PyCharm

**Libraries**
- [`rich`](https://rich.readthedocs.io/) — advanced console formatting (tables, panels, styled text)
- [`requests`](https://requests.readthedocs.io/) — HTTP client for API integration

**Data Persistence**
- JSON file-based storage (no external database required)

**External APIs**
- [Quotable API](https://api.quotable.io) — inspirational quotes
- [Wikipedia REST API](https://en.wikipedia.org/api/rest_v1/) — topic summaries

---

## Architecture

The application follows a **modular, layered design** with clear separation of concerns:

- **`app.py`** acts as an orchestrator — it manages the main loop and delegates work to feature modules, containing no business logic itself.
- **`core/`** holds shared utilities used across the application: a generic API request handler and JSON file manager.
- **`modules/`** contains self-contained feature modules, each responsible for a single domain (goals, motivation, search).
- A single `Console` object is created once in `app.py` and passed into every function that needs it (**dependency injection**), ensuring consistent output formatting throughout the app.

This structure keeps each module independently testable and makes the codebase straightforward to extend — new features can be added as new modules without touching existing code.

---

## Project Structure

```
learning_dashboard/
│
├── app.py                      # Entry point — main menu loop
├── requirements.txt            # Dependencies
│
├── core/
│   ├── api.py                  # HTTP request wrapper with error handling
│   └── file_manager.py         # JSON load/save with corruption recovery
│
├── modules/
│   ├── goals.py                # Goals Manager — core CRUD + algorithms (450+ lines)
│   ├── motivation.py           # Quotable API integration
│   └── search.py               # Wikipedia API integration
│
└── data/
    └── goals.json              # Runtime data storage
```

---

## Data Model

Two entities with a **one-to-many relationship**, connected via a foreign key:

```
Goal                              Session
├─ id                             ├─ id
├─ title                          ├─ goal_id  ──► references Goal.id
├─ description                    ├─ date
├─ category                       ├─ duration_minutes
├─ target_hours                   ├─ topic
├─ deadline                       └─ notes
├─ status
└─ created_at
```

**Key design decision:** progress is *never* stored directly on the `Goal` object. It is always computed on demand by aggregating related sessions. This avoids data inconsistency and keeps a complete history of every study session as the single source of truth.

```python
progress = (total_hours_from_sessions / target_hours) * 100
```

---

## Key Algorithms

### 1. Streak Calculation

Counts consecutive days of study activity by walking backward from today through a set of session dates.

```python
def calculate_streak(sessions: list) -> int:
    if not sessions:
        return 0

    session_dates = {
        datetime.fromisoformat(s['date']).date() for s in sessions
    }

    today = date.today()
    streak = 0
    current_date = today

    while current_date in session_dates:
        streak += 1
        current_date = date.fromordinal(current_date.toordinal() - 1)

    return streak
```

- **Time complexity:** O(n) — n = number of sessions
- **Space complexity:** O(d) — d = number of unique session dates
- Uses a `set` for O(1) date lookups during the backward walk

### 2. Progress Aggregation

Derives a goal's completion percentage from the sum of all its logged sessions, capped at 100%.

```python
def calculate_progress(goal: dict, sessions: list) -> float:
    if goal['target_hours'] == 0:
        return 0

    total_hours = sum(
        s['duration_minutes'] / 60
        for s in sessions if s['goal_id'] == goal['id']
    )

    return min((total_hours / goal['target_hours']) * 100, 100)
```

### 3. Cascade Delete

Removing a goal also removes every session referencing it, preventing orphaned records:

```python
goals = [g for g in goals if g['id'] != goal_id]
sessions = [s for s in sessions if s['goal_id'] != goal_id]
```

A confirmation step (`"yes"` required) protects against accidental deletion.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/D-Ivanova-SZ/personal-learning-dashboard.git
cd personal-learning-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

**Requirements:**
```
requests==2.31.0
rich==13.7.0
```

---

## Usage

1. Launch the app with `python app.py`
2. From the main menu, select **Goals Manager** to create your first goal
3. Log study sessions as you progress — the dashboard updates automatically
4. Check **View Sessions** to see your current streak and full session history
5. Use **Motivation Center** or **Knowledge Search** anytime for a quick break or reference lookup

---

## Error Handling

The application is built to fail gracefully rather than crash:

- **File I/O:** corrupted or missing JSON files are detected and replaced with a safe default structure
- **API calls:** timeouts, connection failures, and HTTP errors are caught individually with clear user-facing messages
- **User input:** a multi-step validation chain (existence checks, type checks, empty-value checks) guards every CRUD operation before data is written

---

## Future Development

The modular architecture makes it straightforward to extend the project without modifying existing code:

- **Analytics module** — progress trends, time distribution, best/worst study days
- **Achievement system** — milestone badges and gamification
- **Notification system** — deadline reminders, streak-risk alerts
- **Export functionality** — CSV/PDF report generation
- **Persistence upgrade** — migration from JSON to SQLite/PostgreSQL
- **Web interface** — Flask/Django front end for the existing core logic

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---
