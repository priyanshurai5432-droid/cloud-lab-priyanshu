#!/usr/bin/env python3
"""
TinyNote - A simple note-taking application
"""

import os
import json
from datetime import datetime

# Store notes in a simple JSON file
NOTES_FILE = "notes.json"


def load_notes():
    """Load notes from file."""
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    return {}


def save_notes(notes):
    """Save notes to file."""
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)


def list_notes(notes):
    """List all notes."""
    if not notes:
        print("No notes yet.")
        return
    for title, content in notes.items():
        print(f"- {title}")


def add_note(notes):
    """Add a new note."""
    title = input("Note title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    content = input("Note content: ").strip()
    notes[title] = {
        "content": content,
        "created": datetime.now().isoformat()
    }
    save_notes(notes)
    print(f"Note '{title}' added.")


def view_note(notes):
    """View a specific note."""
    title = input("Note title to view: ").strip()
    if title in notes:
        note = notes[title]
        print(f"\n--- {title} ---")
        print(note["content"])
        print(f"Created: {note['created']}\n")
    else:
        print(f"Note '{title}' not found.")


def delete_note(notes):
    """Delete a note."""
    title = input("Note title to delete: ").strip()
    if title in notes:
        del notes[title]
        save_notes(notes)
        print(f"Note '{title}' deleted.")
    else:
        print(f"Note '{title}' not found.")


def main():
    """Main application loop."""
    print("Welcome to TinyNote!")
    notes = load_notes()
    
    while True:
        print("\nOptions: (l)ist, (a)dd, (v)iew, (d)elete, (q)uit")
        choice = input("Choose: ").strip().lower()
        
        if choice == "l":
            list_notes(notes)
        elif choice == "a":
            add_note(notes)
        elif choice == "v":
            view_note(notes)
        elif choice == "d":
            delete_note(notes)
        elif choice == "q":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
