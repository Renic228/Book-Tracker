import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker - Трекер прочитанных книг")
        self.root.geometry("800x600")
        
        # Данные книг
        self.books = []
        self.load_data()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Фрейм для формы добавления
        form_frame = ttk.LabelFrame(self.root, text="Добавить книгу")
        form_frame.pack(fill="x", padx=10, pady=5)
        
        # Поля ввода
        ttk.Label(form_frame, text="Название книги:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.title_entry = ttk.Entry(form_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Автор:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.author_entry = ttk.Entry(form_frame, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Жанр:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.genre_entry = ttk.Entry(form_frame, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Количество страниц:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.pages_entry = ttk.Entry(form_frame, width=30)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=2)
        
        # Кнопка добавления
        add_button = ttk.Button(form_frame, text="Добавить книгу", command=self.add_book)
        add_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Фрейм для фильтров
        filter_frame = ttk.LabelFrame(self.root, text="Фильтры")
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Жанр:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.genre_filter = ttk.Combobox(filter_frame, values=["Все", "Роман", "Фантастика", "Детектив", "Биография", "Поэзия"])
        self.genre_filter.set("Все")
        self.genre_filter.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(filter_frame, text="Страниц >:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        self.pages_filter = ttk.Combobox(filter_frame, values=["Все", "200", "300", "500"])
        self.pages_filter.set("Все")
        self.pages_filter.grid(row=0, column=3, padx=5, pady=2)
        
        filter_button = ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        filter_button.grid(row=0, column=4, padx=5, pady=2)
        reset_button = ttk.Button(filter_frame, text="Сбросить", command=self.reset_filter)
        reset_button.grid(row=0, column=5, padx=5, pady=2)
        
        # Таблица для отображения книг
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        columns = ("Название", "Автор", "Жанр", "Страниц")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Кнопки сохранения/загрузки
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        save_button = ttk.Button(button_frame, text="Сохранить в JSON", command=self.save_data)
        save_button.pack(side="left", padx=5)
        load_button = ttk.Button(button_frame, text="Загрузить из JSON", command=self.load_data_from_file)
        load_button.pack(side="left", padx=5)
        
        self.update_table()
    
    def validate_input(self):
        """Проверка корректности ввода"""
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages_text = self.pages_entry.get().strip()
        
        if not title or not author or not genre:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return False
        
        try:
            pages = int(pages_text)
            if pages <= 0:
                messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return False
        
        return True, title, author, genre, pages
    
    def add_book(self):
        """Добавление книги"""
        validation_result = self.validate_input()
        if not validation_result:
            return
        
        is_valid, title, author, genre, pages = validation_result
        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages
        }
        self.books.append(book)
        self.update_table()
        # Очистка полей ввода
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)
    
    def update_table(self, filtered_books=None):
        """Обновление таблицы книг"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        books_to_show = filtered_books if filtered_books is not None else self.books
        for book in books_to_show:
            self.tree.insert("", "end", values=(
                book["title"],
                book["author"],
                book["genre"],
                book["pages"]
            ))
    
    def apply_filter(self):
        """Применение фильтров"""
        genre_filter = self.genre_filter.get()
        pages_filter = self.pages_filter.get()
        filtered_books = self.books.copy()
        
        if genre_filter != "Все":
            filtered_books = [b for b in filtered_books if b["genre"] == genre_filter
        
        if pages_filter != "Все":
            min_pages = int(pages_filter)
            filtered_books