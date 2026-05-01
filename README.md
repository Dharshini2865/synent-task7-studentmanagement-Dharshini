# synent-task7-studentmanagement-Dharshini
# 🎓 Student Management System

A full-featured terminal application to manage student records with CRUD operations, statistics, and CSV storage.

## Features
- Add students with auto-generated IDs (STU001, STU002, ...)
- View all students in a color-coded formatted table
- Search students by name, ID, or grade
- Update student details — name, age, marks, email
- Delete students by ID
- Sort students by name, marks, or grade
- Class statistics — average marks and top 3 students
- Auto-grade calculation from marks
- Duplicate email detection
- Export backup to `students_backup.csv`
- All data saved in `students.csv`

## Requirements
```bash
pip install colorama
```

## How to Run
```bash
python student_management.py
```

## How to Use
1. Run the program — existing student records load automatically
2. Choose from the menu:
   - **1** — View all students + statistics
   - **2** — Add a new student
   - **3** — Search by name, ID, or grade
   - **4** — Update a student's details
   - **5** — Delete a student
   - **6** — Sort the student list
   - **7** — Export a CSV backup
   - **8** — Exit

## Grading Scale
| Marks  | Grade |
|--------|-------|
| 90–100 | A     |
| 75–89  | B     |
| 60–74  | C     |
| 40–59  | D     |
| 0–39   | F     |


## Data Storage

Student records are stored in `students.csv` in the same folder.
A sample `students.csv` is included in this repo with demo data.
The file is created automatically when the first student is added if it doesn't exist.

## Technologies Used
- Python 3
- `csv` — persistent student data storage
- `datetime` — record timestamps
- `colorama` — colored terminal output

## Authors 
Dharshini | Synent Technologies Internship 2026
