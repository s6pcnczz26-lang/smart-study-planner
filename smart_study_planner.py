"""
Smart Study Planner
--------------------
A console-based program for logging, reviewing, and analysing study
sessions across subjects. Data is kept in SESSIONS while the program
runs, and persisted to LOG_FILE so it survives between runs.
"""


import json
import os


import os
import json


SESSIONS = []

LOG_FILE = "study_log.txt"


def main():
    """Show the menu on a loop and dispatch to the right function
    until the user chooses to save and exit."""
    load_sessions()
 
    while True:
        print("\n===== Smart Study Planner =====")
        print("1. Add a study session")
        print("2. View all sessions")
        print("3. Search sessions by subject")
        print("4. View statistics")
        print("5. Save and exit")
 
        choice = input("Choose an option (1-5): ").strip()
 
        if choice == "1":
            add_session()
        elif choice == "2":
            view_sessions()
        elif choice == "3":
            subject = input("Enter a subject to search for: ").strip()
            search_by_subject(subject)
        elif choice == "4":
            study_statistics()
        elif choice == "5":
            save_sessions()
            print("Sessions saved. Goodbye!")
            break
        else:
            # Anything that isn't 1-5 lands here - the loop just goes round again instead of crashing.
            print("That's not a valid option - please enter a number from 1 to 5.")


def add_session():
    """Prompt for a subject, topic, date/day label and duration,
    validate the duration, and append the new session to SESSIONS."""
    subject = input("Subject: ").strip()
    topic = input("Topic covered: ").strip()
    date = input("Date (or day label, e.g. 'Monday'): ").strip()

    while True:
        raw = input("Duration in minutes: ").strip()
        try:
            duration = float(raw)
        except ValueError:
            # float() raises ValueError on anything that isn't a number,
            # so we catch that and print a message, then continue the loop.
            print("Please enter a number.")
            continue
        if duration <= 0:
            print("Duration must be a positive number.")
            continue
        break            

    SESSIONS.append({
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration,
    })
    print(f"Added: {subject} - {topic} ({classify_session(duration)})")


def classify_session(duration):
    """Return 'Short', 'Medium' or 'Long' for a duration in minutes."""
    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"


def print_session_table(sessions):
    """Print a list of sessions as a formatted table. Pulled out as its own function because both view_sessions() and
    search_by_subject() need to print the same kind of table."""
    header = f"{'Subject':<15}{'Topic':<20}{'Duration':<12}{'Classification':<15}"
    print(header)
    print("-" * len(header))
    for session in sessions:
        duration_label = f"{session['duration']:.0f} min"
        session_type = classify_session(session["duration"])
        print(f"{session['subject']:<15}{session['topic']:<20}{duration_label:<12}{session_type:<15}")   


def view_sessions():
    """Print every session in SESSIONS as a formatted table."""
    if not SESSIONS:
        print("No sessions logged yet.")
        return
    print_session_table(SESSIONS)


def search_by_subject(subject):
    """Print sessions matching `subject` (case-insensitive) and their combined duration, or a message if there are none."""
    matches = [s for s in SESSIONS if s["subject"].lower() == subject.lower()]
 
    if not matches:
        print(f"No sessions found for '{subject}'.")
        return
 
    print_session_table(matches)
    total = sum(s["duration"] for s in matches)
    print(f"\nTotal time spent on '{subject}': {total:.0f} min")


def study_statistics():
    """Print total hours overall, total hours per subject, the weakest subject, and the single longest session."""
    if not SESSIONS:
        print("No sessions logged yet - nothing to summarise.")
        return
    
    minutes_per_subject = {}
    for session in SESSIONS:
        subject = session["subject"]
        minutes_per_subject[subject] = minutes_per_subject.get(subject, 0) + session["duration"]

    total_minutes = sum(minutes_per_subject.values())
    print(f"Total time studied: {total_minutes / 60:.1f} hours")

    print("\nTime per subject:")
    for subject in sorted(minutes_per_subject):
        print(f"  {subject}: {minutes_per_subject[subject] / 60:.1f} hours")
 
    # min() over the subject names, comparing each by its total minutes.
    weakest_subject = min(minutes_per_subject, key=minutes_per_subject.get)
    print(f"\nWeakest area (least time spent): {weakest_subject}")
 
    # max() over the raw session list, comparing by duration directly.
    longest = max(SESSIONS, key=lambda s: s["duration"])
    print(f"Longest session: {longest['subject']} - {longest['topic']} "
          f"({longest['duration']:.0f} min, {classify_session(longest['duration'])})")
 

def save_sessions():
    """Write every session in SESSIONS to LOG_FILE."""
    with open(LOG_FILE, "w") as f:
        for session in SESSIONS:
            f.write(f"{session['subject']}|{session['topic']}|{session['date']}|{session['duration']}\n")
 
 
def load_sessions():
    """Load sessions from LOG_FILE into SESSIONS, if the file exists."""
    try:
        with open(LOG_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                subject, topic, date, duration = line.split("|")
                SESSIONS.append({
                    "subject": subject,
                    "topic": topic,
                    "date": date,
                    "duration": float(duration),
                })
    except FileNotFoundError:
        pass
 
 
if __name__ == "__main__":
    main()
  