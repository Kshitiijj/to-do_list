import tkinter as tk  #used for creating GUI
from tkinter import messagebox #used for displayiing message boxes
import sqlite3 #is a library that provides a SQL interface for SQLite databases

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")

        self.conn = sqlite3.connect('tasks.db') #this establishes connection
        self.create_table()

        self.tasks = []
        self.load_tasks()

        self.task_var = tk.StringVar()

        self.setup_ui()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    completed BOOLEAN NOT NULL DEFAULT 0
                )
            """)

    def load_tasks(self):
        with self.conn:
            cursor = self.conn.execute("SELECT id, task, completed FROM tasks")
            self.tasks = [(row[0], row[1], row[2]) for row in cursor.fetchall()]

    def setup_ui(self):
        self.task_entry = tk.Entry(self.root, textvariable=self.task_var)
        self.task_entry.pack(pady=10)

        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=10)

        self.task_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.task_listbox.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        self.task_listbox.bind('<Double-Button-1>', self.edit_task)

        self.delete_button = tk.Button(self.root, text="Delete Completed", command=self.delete_completed)
        self.delete_button.pack(pady=10)

        self.populate_tasks()

    def populate_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            display_text = f"{task[1]} {'(Completed)' if task[2] else ''}"
            self.task_listbox.insert(tk.END, display_text)

    def add_task(self):
        task = self.task_var.get().strip()
        if task:
            with self.conn:
                self.conn.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
            self.task_var.set("")
            self.load_tasks()
            self.populate_tasks()
        else:
            messagebox.showwarning("Warning", "Task cannot be empty!")

    def edit_task(self, event):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_id, task_text, completed = self.tasks[selected_index[0]]
            new_task_text = self.task_var.get().strip()
            if new_task_text:
                with self.conn:
                    self.conn.execute("UPDATE tasks SET task = ? WHERE id = ?", (new_task_text, task_id))
                self.load_tasks()
                self.populate_tasks()
                self.task_var.set("")
            else:
                messagebox.showwarning("Warning", "Task cannot be empty!")

    def delete_completed(self):
        with self.conn:
            self.conn.execute("DELETE FROM tasks WHERE completed = 1")
        self.load_tasks()
        self.populate_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
