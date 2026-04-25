import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.trainings = []
        self.load_data()

        # Создаём виджеты
        self.create_widgets()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=5)
        self.type_entry = ttk.Combobox(self.root, values=["Кардио", "Силовая", "Йога", "Растяжка", "Функциональная"])
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Длительность (мин):").grid(row=2, column=0, padx=5, pady=5)
        self.duration_entry = tk.Entry(self.root)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавления
        tk.Button(self.root, text="Добавить тренировку", command=self.add_training).grid(row=3, column=0, columnspan=2, pady=10)

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("Дата", "Тип", "Длительность"), show="headings")
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Тип", text="Тип")
        self.tree.heading("Длительность", text="Длительность (мин)")
        self.tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Фильтры
        tk.Label(self.root, text="Фильтр по типу:").grid(row=5, column=0, padx=5, pady=5)
        self.filter_type = ttk.Combobox(self.root, values=["Все", "Кардио", "Силовая", "Йога", "Растяжка", "Функциональная"])
        self.filter_type.set("Все")
        self.filter_type.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Фильтр по дате (ДД.ММ.ГГГГ):").grid(row=6, column=0, padx=5, pady=5)
        self.filter_date = tk.Entry(self.root)
        self.filter_date.grid(row=6, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Применить фильтры", command=self.apply_filters).grid(row=7, column=0, columnspan=2, pady=10)

    def validate_input(self):
        try:
            date = datetime.strptime(self.date_entry.get(), "%d.%m.%Y")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ДД.ММ.ГГГГ")
            return False

        try:
            duration = int(self.duration_entry.get())
            if duration <= 0:
                messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть числом")
            return False

        if not self.type_entry.get():
            messagebox.showerror("Ошибка", "Выберите тип тренировки")
            return False

        return True

    def add_training(self):
        if self.validate_input():
            training = {
                "date": self.date_entry.get(),
                "type": self.type_entry.get(),
                "duration": int(self.duration_entry.get())
            }
            self.trainings.append(training)
            self.update_table()
            self.save_data()
            # Очищаем поля ввода
            self.date_entry.delete(0, tk.END)
            self.type_entry.set("")
            self.duration_entry.delete(0, tk.END)

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for training in self.trainings:
            self.tree.insert("", "end", values=(training["date"], training["type"], training["duration"]))

    def apply_filters(self):
        filtered = self.trainings
        filter_type = self.filter_type.get()
        filter_date = self.filter_date.get()

        if filter_type != "Все":
            filtered = [t for t in filtered if t["type"] == filter_type]
        if filter_date:
            try:
                datetime.strptime(filter_date, "%d.%m.%Y")
                filtered = [t for t in filtered if t["date"] == filter_date]
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат даты для фильтра")
                return

        for item in self.tree.get_children():
            self.tree.delete(item)
        for training in filtered:
            self.tree.insert("", "end", values=(training["date"], training["type"], training["duration"]))

    def save_data(self):
        with open("trainings.json", "w", encoding="utf-8") as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=4)

    def load_data(self):
        try:
            with open("trainings.json", "r", encoding="utf-8") as f:
                self.trainings = json.load(f)
        except FileNotFoundError:
            self.trainings = []

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
