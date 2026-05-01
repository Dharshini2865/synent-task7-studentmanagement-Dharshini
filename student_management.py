import csv
import os
from datetime import datetime
from colorama import init, Fore, Style
init(autoreset=True)

FILE = "students.csv"
FIELDS = ["id", "name", "age", "grade", "email", "marks", "added"]


def show_banner():
    print(Fore.CYAN + "=" * 58)
    print(Fore.CYAN + "   STUDENT MANAGEMENT SYSTEM — FINAL VERSION")
    print(Fore.CYAN + "=" * 58)


# ── File helpers ──────────────────────────────────────────────

def load_students():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r", newline="") as f:
        return list(csv.DictReader(f))


def save_students(students):
    with open(FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(students)


def next_id(students):
    if not students:
        return "STU001"
    last = max(int(s["id"].replace("STU", "")) for s in students)
    return f"STU{last + 1:03d}"


# ── Helpers ───────────────────────────────────────────

def grade_color(grade):
    return {
        "A": Fore.GREEN,
        "B": Fore.CYAN,
        "C": Fore.YELLOW,
        "D": Fore.RED,
        "F": Fore.RED
    }.get(grade.upper(), Fore.WHITE)


def marks_to_grade(marks):
    m = float(marks)
    if m >= 90: return "A"
    if m >= 75: return "B"
    if m >= 60: return "C"
    if m >= 40: return "D"
    return "F"


# ── Display ───────────────────────────────────────────

def print_table(students):
    if not students:
        print(Fore.YELLOW + "\n  No students found.")
        return

    print()
    print(Fore.CYAN + f"  {'ID':<8} {'Name':<20} {'Age':<5} {'Grade':<7} {'Marks':<7} {'Email'}")
    print(Fore.CYAN + "  " + "-" * 58)

    for s in students:
        gc = grade_color(s["grade"])
        print(
            Fore.WHITE + f"  {s['id']:<8} "
            + Fore.WHITE + f"{s['name']:<20} "
            + Fore.WHITE + f"{s['age']:<5} "
            + gc + f"{s['grade']:<7} "
            + Fore.WHITE + f"{s['marks']:<7} "
            + Fore.WHITE + Style.DIM + f"{s['email']}"
        )
    print()


def print_stats(students):
    if not students:
        return

    marks = [float(s["marks"]) for s in students]
    avg = sum(marks) / len(marks)

    print(Fore.CYAN + "\n  ── Class Statistics ─────────────────────────")
    print(Fore.WHITE + f"  Total students : {len(students)}")
    print(Fore.WHITE + f"  Average marks  : {avg:.1f}")

    top_students = sorted(students, key=lambda s: float(s["marks"]), reverse=True)[:3]

    print(Fore.GREEN + "  Top 3 students:")
    for i, s in enumerate(top_students, 1):
        print(Fore.GREEN + f"  {i}. {s['name']} ({s['marks']})")


# ── CRUD ─────────────────────────────────────────────

def add_student(students):
    print(Fore.CYAN + "\n  ── Add New Student ──────────────────────────\n")

    while True:
        name = input(Fore.YELLOW + "  Full name      : ").strip()
        if len(name) >= 2:
            break
        print(Fore.RED + "  Name must be at least 2 characters.")

    while True:
        try:
            age = int(input(Fore.YELLOW + "  Age            : "))
            if 5 <= age <= 100:
                break
        except:
            pass
        print(Fore.RED + "  Invalid age.")

    # Duplicate email check
    while True:
        email = input(Fore.YELLOW + "  Email          : ").strip()
        if "@" not in email or "." not in email:
            print(Fore.RED + "  Invalid email.")
            continue
        if any(s["email"] == email for s in students):
            print(Fore.RED + "  Email already exists.")
            continue
        break

    while True:
        try:
            marks = float(input(Fore.YELLOW + "  Marks (0-100)  : "))
            if 0 <= marks <= 100:
                break
        except:
            pass
        print(Fore.RED + "  Invalid marks.")

    grade = marks_to_grade(marks)

    student = {
        "id": next_id(students),
        "name": name,
        "age": str(age),
        "grade": grade,
        "email": email,
        "marks": str(marks),
        "added": datetime.now().strftime("%d %b %Y")
    }

    students.append(student)
    save_students(students)

    print(Fore.GREEN + f"\n  ✓ Student added! ID: {student['id']}")
    return students


def view_students(students):
    print(Fore.CYAN + "\n  ── All Students ─────────────────────────────")
    print_table(students)
    print_stats(students)


def search_student(students):
    print(Fore.CYAN + "\n  ── Search Students ──────────────────────────\n")
    query = input(Fore.YELLOW + "  Enter name/id/grade: ").lower()

    results = [
        s for s in students
        if query in s["name"].lower()
        or query in s["id"].lower()
        or query == s["grade"].lower()
    ]

    print_table(results)


def update_student(students):
    print(Fore.CYAN + "\n  ── Update Student ───────────────────────────\n")
    sid = input(Fore.YELLOW + "  Enter Student ID: ").upper()

    student = next((s for s in students if s["id"] == sid), None)
    if not student:
        print(Fore.RED + "  Not found.")
        return students

    print(Fore.WHITE + "  Press Enter to skip\n")

    name = input(f"  Name [{student['name']}]: ")
    if name:
        student["name"] = name

    age = input(f"  Age [{student['age']}]: ")
    if age.isdigit():
        student["age"] = age

    marks = input(f"  Marks [{student['marks']}]: ")
    if marks:
        try:
            m = float(marks)
            student["marks"] = marks
            student["grade"] = marks_to_grade(m)
        except:
            pass

    email = input(f"  Email [{student['email']}]: ")
    if email and "@" in email:
        student["email"] = email

    save_students(students)
    print(Fore.GREEN + "  ✓ Updated successfully!")
    return students


def delete_student(students):
    print(Fore.CYAN + "\n  ── Delete Student ───────────────────────────\n")
    sid = input(Fore.YELLOW + "  Enter Student ID: ").upper()

    new_list = [s for s in students if s["id"] != sid]

    if len(new_list) == len(students):
        print(Fore.RED + "  Not found.")
    else:
        save_students(new_list)
        print(Fore.GREEN + "  ✓ Deleted successfully!")

    return new_list


# ── EXTRA FEATURES ─────────────────────────────────

def sort_students(students):
    print(Fore.CYAN + "\n  ── Sort Students ───────────────────────────\n")
    print("  1. Name\n  2. Marks\n  3. Grade")

    choice = input(Fore.YELLOW + "  Choice: ")

    if choice == "1":
        students.sort(key=lambda x: x["name"].lower())
    elif choice == "2":
        students.sort(key=lambda x: float(x["marks"]), reverse=True)
    elif choice == "3":
        students.sort(key=lambda x: x["grade"])
    else:
        print(Fore.RED + "  Invalid choice")
        return

    print(Fore.GREEN + "  ✓ Sorted!")


def export_backup(students):
    with open("students_backup.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(students)

    print(Fore.GREEN + "  ✓ Backup saved!")


# ── MENU ───────────────────────────────────────────

def show_menu():
    print(Fore.CYAN  + "\n  MENU")
    print(Fore.GREEN + "  1. View all students")
    print(Fore.GREEN + "  2. Add a student")
    print(Fore.GREEN + "  3. Search students")
    print(Fore.GREEN + "  4. Update a student")
    print(Fore.GREEN + "  5. Delete a student")
    print(Fore.GREEN + "  6. Sort students")
    print(Fore.GREEN + "  7. Export backup")
    print(Fore.RED   + "  8. Exit")
    print()


def main():
    show_banner()
    students = load_students()

    while True:
        show_menu()
        choice = input(Fore.YELLOW + "  Enter choice (1-8): ").strip()

        if choice == "1": view_students(students)
        elif choice == "2": students = add_student(students)
        elif choice == "3": search_student(students)
        elif choice == "4": students = update_student(students)
        elif choice == "5": students = delete_student(students)
        elif choice == "6": sort_students(students)
        elif choice == "7": export_backup(students)
        elif choice == "8":
            print(Fore.CYAN + "\n  Goodbye 👋\n")
            break
        else:
            print(Fore.RED + "  Invalid choice.")

        print(Fore.CYAN + "  " + "-" * 56)


if __name__ == "__main__":
    main()