import tkinter as tk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_number TEXT NOT NULL,
    marks REAL NOT NULL
)
""")
conn.commit()

root = tk.Tk()
root.title("Student Management System")
root.geometry("500x450")

tk.Label(root, text="Student Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Roll Number").pack()
roll_entry = tk.Entry(root)
roll_entry.pack()

tk.Label(root, text="Marks").pack()
marks_entry = tk.Entry(root)
marks_entry.pack()

def save_student():
    name = name_entry.get().strip()
    roll = roll_entry.get().strip()
    marks = marks_entry.get().strip()

    if not name or not roll or not marks:
        messagebox.showerror("Error", "Fill all fields")
        return

    try:
        marks = float(marks)
        if not 0 <= marks <= 100:
            messagebox.showerror(
                "Error", "Marks must be between 0 and 100"
            )
            return
    except ValueError:
        messagebox.showerror("Error", "Enter valid marks")
        return

    cursor.execute(
        """INSERT INTO students
        (name, roll_number, marks) VALUES (?, ?, ?)""",
        (name, roll, marks)
    )
    conn.commit()

    messagebox.showinfo("Success", "Student saved successfully!")
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)

def view_students():
    cursor.execute(
        "SELECT id, name, roll_number, marks FROM students"
    )
    records = cursor.fetchall()

    if not records:
        messagebox.showinfo("Students", "No student records found")
        return

    result = tk.Toplevel(root)
    result.title("Saved Student Details")
    result.geometry("450x300")

    text = tk.Text(result, width=52, height=15)
    text.pack(padx=10, pady=10)

    text.insert(tk.END, "ID | Name | Roll Number | Marks\n")
    text.insert(tk.END, "-" * 45 + "\n")

    for student in records:
        text.insert(
            tk.END,
            f"{student[0]} | {student[1]} | "
            f"{student[2]} | {student[3]}\n"
        )

    text.config(state="disabled")

tk.Button(
    root, text="Save Student", command=save_student
).pack(pady=10)

tk.Button(
    root, text="View All Students", command=view_students
).pack(pady=5)

root.mainloop()
conn.close()