# 📚 Personal Learning Dashboard

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

A modular Python console application for managing learning goals and tracking study sessions with JSON persistence,
progress analytics, study streak calculation, and REST API integrations.

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Project Structure](#-project-structure)
- [Technologies](#-technologies)
- [Installation](#-installation)
- [Example Workflow](#-example-workflow)
- [Technical Highlights](#-technical-highlights)
- [Future Improvements](#-future-improvements)
- [Learning Objectives](#learning-objectives)
- [License](#-license)

---

## 🎯 Overview

Personal Learning Dashboard helps users organize their learning journey by creating learning goals, logging study sessions, and monitoring progress over time.

The application stores all data locally in JSON format and provides a clean terminal interface built with the Rich library.

---

## ✨ Features

- Create and manage learning goals
- Log study sessions
- Track progress automatically
- Calculate learning streaks
- View study history
- JSON data persistence
- Motivational quotes (REST API)
- Wikipedia search (REST API)
- Rich terminal UI
- Error handling and input validation

---

## 📸 Screenshots

[Welcome Screen](screenshots/welcome_screen.png) |
[Main Menu](screenshots/main_menu.png) |
[Goals Manager](screenshots/goals_manager.png) |
[View All Goals](screenshots/view_all_goals.png) |
[Log Study Session](screenshots/log_study_session.png) |
[View Session History](screenshots/view_session_history.png) |
[Knowledge Search](screenshots/knowledge_search.png)

---

## 📁 Project Structure

```

learning_dashboard/
│
├── app.py
├── requirements.txt
│
├── core/
│ ├── api.py
│ └── file_manager.py
│
├── modules/
│ ├── goals.py
│ ├── motivation.py
│ └── search.py
│
└── data/
└── goals.json

```

---

## 🛠️ Technologies

- Python 3
- Requests
- Rich
- JSON
- REST APIs

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/D-Ivanova-SZ/personal-learning-dashboard.git

cd personal-learning-dashboard
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

---

## ✨ Example Workflow

1. Create a learning goal.
2. Log study sessions.
3. Track progress automatically.
4. View study history.
5. Monitor your learning streak.

---

## 🛠️ Technical Highlights

### Modular Architecture

The project follows a modular design with clear separation of responsibilities:

- Core utilities
- Feature modules
- Persistent storage
- Main application controller

### Progress Aggregation

Instead of storing completed hours directly, progress is calculated dynamically from all recorded study sessions, ensuring consistency and eliminating duplicated data.

### Study Streak Algorithm

The application calculates consecutive learning days using date arithmetic and session history.

### Persistent Storage

All user data is stored in JSON format and automatically loaded on startup.

---

## ✨ Future Improvements

- Unit tests
- Export statistics
- Dashboard analytics
- SQLite database support
- User authentication
- Graphical interface (Tkinter or Web)

---

# 📚 Learning Objectives

This project was built to practice:

- Python programming
- Modular software architecture
- File handling
- Working with APIs
- Error handling
- Data structures
- CLI application development

---

## 📄 License

This project is available for educational and portfolio purposes.