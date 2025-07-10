import tkinter as tk
from tkinter import messagebox, simpledialog
from person import Person
from storage.json_db import JsonDatabase
from storage.sqlite_db import SQLiteDatabase

root = tk.Tk()
root.title("База Даних Людей")
root.configure(bg="#90D1CA")  # Window background

# --- Variable for selecting storage type ---
storage_type = tk.StringVar(value="json")  # Default — JSON

# --- Function to get the active storage instance ---
def get_db():
    if storage_type.get() == "sqlite":
        return SQLiteDatabase()
    return JsonDatabase()

# --- Main actions ---
def show_all():
    db = get_db()
    db.load_data()
    text_box.delete("1.0", tk.END)
    for person in db.list_all():
        text_box.insert(tk.END, str(person) + "\n\n")

def add_person():
    db = get_db()
    db.load_data()
    try:
        first_name = simpledialog.askstring("Ім'я", "Введіть ім'я:")
        if not first_name:
            raise ValueError("Ім'я обов'язкове.")

        last_name = simpledialog.askstring("Прізвище", "Введіть прізвище (необов’язково):") or ""
        middle_name = simpledialog.askstring("По батькові", "Введіть по батькові (необов’язково):") or ""
        gender = simpledialog.askstring("Стать", "Стать (male/female):").strip().lower()
        birth_date = simpledialog.askstring("Дата народження", "Наприклад: 12.10.1980")
        death_date = simpledialog.askstring("Дата смерті", "Залиш порожнім, якщо жива:") or None

        person = Person(first_name, gender, birth_date, last_name, middle_name, death_date)
        db.add_person(person)
        db.save_data()
        messagebox.showinfo("Успіх", "Людину додано!")
        show_all()
    except Exception as e:
        messagebox.showerror("Помилка", str(e))

def search():
    db = get_db()
    db.load_data()
    query = simpledialog.askstring("Пошук", "Введіть рядок для пошуку:")
    if not query:
        return
    results = db.search(query)
    text_box.delete("1.0", tk.END)
    if results:
        for person in results:
            text_box.insert(tk.END, str(person) + "\n\n")
    else:
        text_box.insert(tk.END, "Нічого не знайдено.")

def save_data():
    db = get_db()
    db.save_data()
    messagebox.showinfo("Збереження", "Дані збережено.")

def load_data():
    db = get_db()
    db.load_data()
    messagebox.showinfo("Завантаження", "Дані завантажено.")
    show_all()

# --- Top section with storage selector ---
top_frame = tk.Frame(root, bg="#90D1CA")
top_frame.pack(pady=10)

tk.Label(top_frame, text="Сховище:", bg="#90D1CA", fg="#096B68").pack(side="left", padx=5)
tk.Radiobutton(top_frame, text="JSON", variable=storage_type, value="json",
               bg="#90D1CA", fg="#096B68", selectcolor="#FFFBDE").pack(side="left")
tk.Radiobutton(top_frame, text="SQLite", variable=storage_type, value="sqlite",
               bg="#90D1CA", fg="#096B68", selectcolor="#FFFBDE").pack(side="left")

# --- Buttons ---
frame = tk.Frame(root, bg="#90D1CA")
frame.pack(pady=10)

btn_bg = "#096B68"
btn_fg = "#FFFBDE"
btn_active_bg = "#129990"
text_box_bg = "#FFFBDE"
text_box_fg = "#096B68"

tk.Button(frame, text="Додати", command=add_person, width=15,
          highlightthickness=0, bg=btn_bg, fg=btn_fg, activebackground=btn_active_bg).grid(row=0, column=0, padx=5)

tk.Button(frame, text="Пошук", command=search, width=15,
          highlightthickness=0, bg=btn_bg, fg=btn_fg, activebackground=btn_active_bg).grid(row=0, column=1, padx=5)

tk.Button(frame, text="Всі записи", command=show_all, width=15,
          highlightthickness=0, bg=btn_bg, fg=btn_fg, activebackground=btn_active_bg).grid(row=0, column=2, padx=5)

tk.Button(frame, text="Зберегти", command=save_data, width=15,
          highlightthickness=0, bg=btn_bg, fg=btn_fg, activebackground=btn_active_bg).grid(row=0, column=3, padx=5)

tk.Button(frame, text="Завантажити", command=load_data, width=15,
          highlightthickness=0, bg=btn_bg, fg=btn_fg, activebackground=btn_active_bg).grid(row=0, column=4, padx=5)

# --- Text box ---
text_box = tk.Text(root, height=25, width=100, bg=text_box_bg, fg=text_box_fg,
                   highlightthickness=0, padx=20, pady=10)
text_box.pack(padx=10, pady=10)

# --- Show initial data ---
show_all()

root.mainloop()
