Smart Study Planner

A console-based Python program for logging, reviewing, and analysing study sessions across different subjects. Built for the Programming Fundamentals (1203 ST) coursework at Victoria University.

Features
Add a study session (subject, topic, date, duration)
View all logged sessions in a formatted table, with each session classified as Short, Medium, or Long
Search sessions by subject (case-insensitive), with total time spent shown
View statistics: total hours studied, hours per subject, weakest subject, and the longest single session
Sessions persist between runs via study_log.txt
Requirements

Python 3. No external libraries needed.

Running It
python3 smart_study_planner.py

Follow the on-screen menu (options 1–5). Choosing "Save and exit" writes all sessions to study_log.txt, which is automatically reloaded the next time the program starts.

How Sessions Are Stored

Each session is a dictionary with subject, topic, date, and duration fields, kept in a single list for the length of the program's run. On exit, sessions are saved to study_log.txt one per line, with fields separated by |. If that file doesn't exist yet, the program just starts with an empty session list.

## Author

Name: KATONGOLE IBRAHIM SSEMATA

Module: Programming Fundamentals

Module Code: 1203 ST

Level: 1.2
