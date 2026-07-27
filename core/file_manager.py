"""
File Manager Module
Handles JSON file operations for persistent data storage
"""

import json
import os
from typing import Dict, Any

DATA_FILE = "data/goals.json"


def ensure_data_dir() -> None:
    """
    Creates 'data' directory if it doesn't exist.
    With exist_ok=True no errors are thrown if directory already exists.
    """

    os.makedirs("data", exist_ok=True)


def load_data() -> Dict[str, Any]:
    """
    Loads all data from JSON file.
    Returns empty structure if file doesn't exist.

    Returned format is:
        {
            'goals': [list of goal dictionaries],
            'sessions': [list of session dictionaries]
        }
    """

    ensure_data_dir()

    if not os.path.exists(DATA_FILE):
        return {"goals": [], "sessions": []}

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    except json.JSONDecodeError:
        print("Warning: Invalid JSON file, starting fresh")
        return {"goals": [], "sessions": []}

    except Exception as e:
        print(f"Error loading data: {e}")
        return {"goals": [], "sessions": []}


def save_data(data: Dict[str, Any]) -> bool:
    """
    Saves data to JSON file.
    It accepts dictionary containing goals and sessions
    """

    ensure_data_dir()

    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            # indent=2: for formatting
            # ensure_ascii=False: allows unicode (cyrillic, etc.)
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True

    except Exception as e:
        print(f"Error saving data: {e}")
        return False
