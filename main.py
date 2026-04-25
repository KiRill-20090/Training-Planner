import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")
        
        # Путь к JSON файлу
        self.data_file = "movies.json"
        
        # Загрузка данных
        self.movies = self.load_movies()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Отображение всех фильмов при запуске
        self.display_movies(self.movies)
    
    def load_movies(self):
        """Загрузка данных из JSON файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                messagebox.showerror("Ошибка", "Ошибка чтения файла данных")
                return []
        return []
    
    def save_movies(self):
        """Сохранение данных в JSON файл"""
        with open(self.data_file, 'w', encoding='utf-8') as file:
            json.dump(self.movies, file, ensure_ascii=False, indent=4)
    
    def create_widgets(self):
        """Создание всех виджетов интерфейса"""
        
        # Заголовок
        title_label = tk.Label(
            self.root, 
            text="MOVIE LIBRARY", 
            font=("Arial", 24, "bold"), 
            bg="#f0f0f0", 
            fg="#333333"
        )
        title_label.pack(pady=10)
        
        # Фрейм для ввода данных
        input_frame = tk.Frame(self.root, bg="#f0f0f0", relief=tk.RAISED, borderwidth=2)
        input_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Поля ввода
        # Название
        tk.Label(input_frame, text="Название:", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.title_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.title_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Жанр
        tk.Label(input_frame, text="Жанр:", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=2, sticky="w", pady=5, padx=5)
        self.genre_entry = tk.Entry(input_frame, width=20, font=("Arial", 10))
        self.genre_entry.grid(row=0, column=3, pady=5, padx=5)
        
        # Год выпуска
        tk.Label(input_frame, text="Год выпуска:", bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.year_entry = tk.Entry(input_frame, width=15, font=("Arial", 10))
        self.year_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Рейтинг
        tk.Label(input_frame, text="Рейтинг (0-10):", bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=2, sticky="w", pady=5, padx=5)
        self.rating_entry = tk.Entry(input_frame, width=15, font=("Arial", 10))
        self.rating_entry.grid(row=1, column=3, pady=5, padx=5)
        
        # Кнопка добавления
        add_button = tk.Button(
            input_frame, 
            text="Добавить фильм", 
            command=self.add_movie,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20
        )
        add_button.grid(row=2, column=0, columnspan=4, pady=15)
        
        # Фрейм для фильтрации
        filter_frame = tk.Frame(self.root, bg="#f0f0f0", relief=tk.RAISED, borderwidth=2)
        filter_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(
            filter_frame, 
            text="ФИЛЬТРАЦИЯ", 
            bg="#f0f0f0", 
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, columnspan=4, pady=5)
        
        # Фильтр по жанру
        tk.Label(filter_frame, text="По жанру:", bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.filter_genre_entry = tk.Entry(filter_frame, width=20, font=("Arial", 10))
        self.filter_genre_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Фильтр по году
        tk.Label(filter_frame, text="По году:", bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=2, sticky="w", pady=5, padx=5)
        self.filter_year_entry = tk.Entry(filter_frame, width=15, font=("Arial", 10))
        self.filter_year_entry.grid(row=1, column=3, pady=5, padx=5)
        
        # Кнопки фильтрации
        filter_button = tk.Button(
            filter_frame, 
            text="Применить фильтр", 
            command=self.apply_filter,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10)
        )
        filter_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        reset_button = tk.Button(
            filter_frame, 
            text="Сбросить фильтр", 
            command=self.reset_filter,
            bg="#FF5722",
            fg="white",
            font=("Arial", 10)
        )
        reset_button.grid(row=2, column=2, columnspan=2, pady=10)
        
        # Фрейм для таблицы
        table_frame = tk.Frame(self.root, relief=tk.RAISED, borderwidth=2)
        table_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Создание таблицы
        columns = ("Название", "Жанр", "Год выпуска", "Рейтинг")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Настройка столбцов
        self.tree.heading("Название", text="Название")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Год выпуска", text="Год выпуска")
        self.tree.heading("Рейтинг", text="Рейтинг")
        
        self.tree.column("Название", width=300)
        self.tree.column("Жанр", width=200)
        self.tree.column("Год выпуска", width=150)
        self.tree.column("Рейтинг", width=100)
        
        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Кнопка удаления
        delete_button = tk.Button(
            self.root,
            text="Удалить выбранный фильм",
            command=self.delete_movie,
            bg="#F44336",
            fg="white",
            font=("Arial", 10)
        )
        delete_button.pack(pady=5)
        
        # Информационная метка
        self.info_label = tk.Label(
            self.root, 
            text=f"Всего фильмов: {len(self.movies)}", 
            bg="#f0f0f0", 
            font=("Arial", 9, "italic")
        )
        self.info_label.pack(pady=5)
    
    def add_movie(self):
        """Добавление нового фильма"""
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()
        
        # Проверка заполнения всех полей
        if not title or not genre:
            messagebox.showerror("Ошибка", "Название и жанр обязательны для заполнения!")
            return
        
        # Проверка года
        if not year:
            messagebox.showerror("Ошибка", "Год выпуска обязателен для заполнения!")
            return
        
        try:
            year_int = int(year)
            if year_int < 1888 or year_int > datetime.now().year:
                messagebox.showerror("Ошибка", f"Год должен быть между 1888 и {datetime.now().year}!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом!")
            return
        
        # Проверка рейтинга
        if not rating:
            messagebox.showerror("Ошибка", "Рейтинг обязателен для заполнения!")
            return
        
        try:
            rating_float = float(rating)
            if rating_float < 0 or rating_float > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом!")
            return
        
        # Создание объекта фильма
        movie = {
            "title": title,
            "genre": genre,
            "year": year_int,
            "rating": rating_float
        }
        
        # Добавление фильма
        self.movies.append(movie)
        self.save_movies()
        
        # Очистка полей ввода
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)
        
        # Обновление таблицы
        self.display_movies(self.movies)
        self.update_info_label()
        
        messagebox.showinfo("Успех", f"Фильм '{title}' успешно добавлен!")
    
    def apply_filter(self):
        """Применение фильтрации"""
        filter_genre = self.filter_genre_entry.get().strip().lower()
        filter_year = self.filter_year_entry.get().strip()
        
        filtered_movies = self.movies.copy()
        
        # Фильтрация по жанру
        if filter_genre:
            filtered_movies = [
                movie for movie in filtered_movies 
                if filter_genre in movie["genre"].lower()
            ]
        
        # Фильтрация по году
        if filter_year:
            try:
                year_int = int(filter_year)
                filtered_movies = [
                    movie for movie in filtered_movies 
                    if movie["year"] == year_int
                ]
            except ValueError:
                messagebox.showerror("Ошибка", "Год в фильтре должен быть числом!")
                return
        
        self.display_movies(filtered_movies)
        
        if not filtered_movies:
            messagebox.showinfo("Информация", "Фильмы не найдены по заданным критериям")
    
    def reset_filter(self):
        """Сброс фильтрации"""
        self.filter_genre_entry.delete(0, tk.END)
        self.filter_year_entry.delete(0, tk.END)
        self.display_movies(self.movies)
    
    def delete_movie(self):
        """Удаление выбранного фильма"""
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите фильм для удаления!")
            return
        
        # Получение данных выбранного фильма
        item = self.tree.item(selected_item[0])
        values = item['values']
        
        if messagebox.askyesno("Подтверждение", f"Удалить фильм '{values[0]}'?"):
            # Поиск и удаление фильма
            self.movies = [
                movie for movie in self.movies 
                if not (movie["title"] == values[0] and 
                       movie["genre"] == values[1] and 
                       movie["year"] == int(values[2]) and 
                       movie["rating"] == float(values[3]))
            ]
            
            self.save_movies()
            self.display_movies(self.movies)
            self.update_info_label()
    
    def display_movies(self, movies_to_display):
        """Отображение фильмов в таблице"""
        # Очистка текущего содержимого таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Добавление фильмов в таблицу
        for movie in movies_to_display:
            self.tree.insert("", tk.END, values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                movie["rating"]
            ))
    
    def update_info_label(self):
        """Обновление информационной метки"""
        self.info_label.config(text=f"Всего фильмов: {len(self.movies)}")

def main():
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()

if __name__ == "__main__":
    main()
