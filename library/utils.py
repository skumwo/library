from .models import Book, Student, Pupil
import pickle
import os

def export_books_to_txt(filename="books.txt"):
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

# library/utils.py
import pickle
from .models import Book, Student, Pupil

def serialize_library(filename="library.pkl"):
    """Сериализация книг и пользователей с информацией о заимствованных книгах."""
    data = {
        "books": list(Book.objects.all()),
        "students": [],
        "pupils": [],
        "borrowed_data": {}  # Словарь для хранения информации о заимствованиях
    }

    for student in Student.objects.prefetch_related('borrowed_books'):
        student_data = {
            'id': student.id,
            'user_id': student.user_id,
            'name': student.name,
            'surname': student.surname,
            'group': student.group,
            'borrowed_book_ids': [book.id for book in student.borrowed_books.all()]
        }
        data["students"].append(student_data)

    for pupil in Pupil.objects.prefetch_related('borrowed_books'):
        pupil_data = {
            'id': pupil.id,
            'user_id': pupil.user_id,
            'name': pupil.name,
            'surname': pupil.surname,
            'group': pupil.group,
            'age': pupil.age,
            'borrowed_book_ids': [book.id for book in pupil.borrowed_books.all()]
        }
        data["pupils"].append(pupil_data)

    try:
        with open(filename, "wb") as file:
            pickle.dump(data, file)
        return True
    except Exception as e:
        print(f"Ошибка при сериализации: {e}")
        return False


# library/utils.py
import pickle
from .models import Book, Student, Pupil

def deserialize_library(filename="library.pkl"):
    """Десериализация книг и пользователей с восстановлением информации о заимствованных книгах."""
    try:
        with open(filename, "rb") as file:
            data = pickle.load(file)

            Book.objects.all().delete()
            Student.objects.all().delete()
            Pupil.objects.all().delete()

            books = {book.id: book for book in Book.objects.bulk_create(data["books"])}
            students = []
            for student_data in data["students"]:
                student = Student.objects.create(
                    id=student_data['id'],
                    user_id=student_data['user_id'],
                    name=student_data['name'],
                    surname=student_data['surname'],
                    group=student_data['group']
                )
                students.append(student)
                for book_id in student_data['borrowed_book_ids']:
                    if book_id in books:
                        student.borrowed_books.add(books[book_id])

            pupils = []
            for pupil_data in data["pupils"]:
                pupil = Pupil.objects.create(
                    id=pupil_data['id'],
                    user_id=pupil_data['user_id'],
                    name=pupil_data['name'],
                    surname=pupil_data['surname'],
                    group=pupil_data['group'],
                    age=pupil_data['age']
                )
                pupils.append(pupil)
                for book_id in pupil_data['borrowed_book_ids']:
                    if book_id in books:
                        pupil.borrowed_books.add(books[book_id])

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