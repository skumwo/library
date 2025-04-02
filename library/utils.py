from .models import Book, Student, Pupil
import pickle
import os

def export_books_to_txt(filename="import_books.txt"):
    """Экспорт списка книг в текстовый файл."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            books = Book.objects.all()
            for book in books:
                file.write(f"{book.title},{book.author},{book.isbn},{book.year},{book.quantity},{book.label}\n")
        return True
    except Exception as e:
        print(f"Ошибка при экспорте книг: {e}")
        return False

def import_books_from_txt(filename="books.txt"):
    """Импорт книг из текстового файла."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 6:
                    title, author, isbn, year, quantity, label = parts
                    Book.objects.create(
                        title=title,
                        author=author,
                        isbn=isbn,
                        year=int(year),
                        quantity=int(quantity),
                        label=label,
                    )
        return True
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return False
    except Exception as e:
        print(f"Ошибка при импорте книг: {e}")
        return False

def export_users_to_txt(filename="users.txt"):
    """Экспорт списка пользователей (Student и Pupil) в текстовый файл."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            students = Student.objects.all()
            pupils = Pupil.objects.all()
            for student in students:
                file.write(f"Student,{student.user_id},{student.name},{student.surname},{student.group}\n")
            for pupil in pupils:
                file.write(f"Pupil,{pupil.user_id},{pupil.name},{pupil.surname},{pupil.group},{pupil.age}\n")
        return True
    except Exception as e:
        print(f"Ошибка при экспорте пользователей: {e}")
        return False

def import_users_from_txt(filename="users.txt"):
    """Импорт пользователей (Student и Pupil) из текстового файла."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 5:  # Student
                    user_type, user_id, name, surname, group = parts
                    Student.objects.create(user_id=int(user_id), name=name, surname=surname, group=group)
                elif len(parts) == 6:  # Pupil
                    user_type, user_id, name, surname, group, age = parts
                    Pupil.objects.create(user_id=int(user_id), name=name, surname=surname, group=group, age=int(age))
        return True
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return False
    except Exception as e:
        print(f"Ошибка при импорте пользователей: {e}")
        return False

def serialize_library(filename="library.pkl"):
    """Сериализация книг и пользователей."""
    from .models import Book, Student, Pupil
    data = {
        "books": list(Book.objects.all()),
        "students": list(Student.objects.all()),
        "pupils": list(Pupil.objects.all()),
    }
    try:
        with open(filename, "wb") as file:
            pickle.dump(data, file)
        return True
    except Exception as e:
        print(f"Ошибка при сериализации: {e}")
        return False

def deserialize_library(filename="library.pkl"):
    """Десериализация книг и пользователей."""
    from .models import Book, Student, Pupil  # Импортируем внутри функции
    try:
        with open(filename, "rb") as file:
            data = pickle.load(file)
            Book.objects.all().delete()
            Student.objects.all().delete()
            Pupil.objects.all().delete()
            Book.objects.bulk_create(data["books"])
            Student.objects.bulk_create(data["students"])
            Pupil.objects.bulk_create(data["pupils"])
        return True
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return False
    except Exception as e:
        print(f"Ошибка при десериализации: {e}")
        return False

def drop_all_data():
    """Удаление всех данных (книг и пользователей)."""
    from .models import Book, Student, Pupil
    Book.objects.all().delete()
    Student.objects.all().delete()
    Pupil.objects.all().delete()
    return True