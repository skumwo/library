from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Pupil, Book
from .models import BorrowHistory
from .forms import BookForm, StudentForm, PupilForm
from .forms import UserRegistrationForm
import random

from django.views.decorators.http import require_POST
from django.contrib import messages

def edit_user(request, user_id):
    user = Student.objects.filter(user_id=user_id).first() or Pupil.objects.filter(user_id=user_id).first()
    if not user:
        return redirect('user_list')

    form_class = StudentForm if isinstance(user, Student) else PupilForm

    if request.method == 'POST':
        form = form_class(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = form_class(instance=user)

    return render(request, 'edit_user.html', {'form': form, 'user': user})


def delete_user(request, user_id):
    user = Student.objects.filter(user_id=user_id).first() or Pupil.objects.filter(user_id=user_id).first()
    if not user:
        return redirect('user_list')

    if request.method == 'POST':
        user.delete()
        return redirect('user_list')

    return render(request, 'confirm_delete.html', {'object': user, 'type': 'user'})


def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form, 'book': book})

def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'confirm_delete.html', {'object': book, 'type': 'book'})

@require_POST
def return_single_book(request):
    user_id = int(request.POST.get('user_id'))
    book_id = int(request.POST.get('book_id'))

    user = Student.objects.filter(user_id=user_id).first() or Pupil.objects.filter(user_id=user_id).first()
    if user:
        book = user.borrowed_books.filter(id=book_id).first()
        if book:
            user.borrowed_books.remove(book)

            BorrowHistory.objects.create(
                user_name=f"{user.name} {user.surname}",
                user_id=user.user_id,
                book_title=book.title,
                action='return'
            )

            messages.success(request, f"Book '{book.title}' returned from {user.name} {user.surname}")

    return redirect('borrowed_books')


def home(request):
    return render(request, 'home.html')

def generate_user_id(prefix):
    existing_ids = set(Student.objects.values_list('user_id', flat=True)) | \
                   set(Pupil.objects.values_list('user_id', flat=True))

    all_possible_ids = [int(f"{prefix}{i:04}") for i in range(10000)]
    available_ids = list(set(all_possible_ids) - existing_ids)

    if not available_ids:
        raise Exception("No available user_id")

    return random.choice(available_ids)

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            group = form.cleaned_data['group']
            age = form.cleaned_data['age']

            if age < 18:
                user_id = generate_user_id(1)
                Pupil.objects.create(user_id=user_id, name=name, surname=surname, group=group, age=age)
            else:
                user_id = generate_user_id(2)
                Student.objects.create(user_id=user_id, name=name, surname=surname, group=group)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register_user.html', {'form': form})

def assign_book(request):
    students = Student.objects.all()
    pupils = Pupil.objects.all()
    books = Book.objects.all()

    if request.method == 'POST':
        user_id = int(request.POST.get('user_id'))
        book_id = int(request.POST.get('book_id'))

        user = Student.objects.filter(user_id=user_id).first() or Pupil.objects.filter(user_id=user_id).first()
        book = Book.objects.get(id=book_id)

        borrowed_by_students = book.student_set.count()
        borrowed_by_pupils = book.pupil_set.count()
        total_borrowed = borrowed_by_students + borrowed_by_pupils

        if user is None:
            error = "User not found."
        elif book in user.borrowed_books.all():
            error = f"{user.name} has already borrowed '{book.title}'."
        elif total_borrowed >= book.quantity:
            error = f"'{book.title}' is not available. All copies are borrowed."
        elif isinstance(user, Pupil) and user.age < 7:
            error = f"{user.name} is too young to borrow books (under 7)."
        elif user.borrowed_books.count() >= 5:
            error = f"{user.name} has reached the borrowing limit (5 books max)."
        elif not user.can_borrow(book):
            error = f"{user.name} is not allowed to borrow '{book.title}'."
        else:
            user.borrowed_books.add(book)

            BorrowHistory.objects.create(
                user_name=f"{user.name} {user.surname}",
                user_id=user.user_id,
                book_title=book.title,
                action='borrow'
            )

            return redirect('user_list')

        return render(request, 'assign_book.html', {
            'students': students,
            'pupils': pupils,
            'books': books,
            'error': error
        })

    return render(request, 'assign_book.html', {
        'students': students,
        'pupils': pupils,
        'books': books
    })

def user_list(request):
    students = Student.objects.all()
    pupils = Pupil.objects.all()
    users = list(students) + list(pupils)
    users.sort(key=lambda x: x.user_id)
    return render(request, 'user_list.html', {'users': users})


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

def book_list(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'book_list.html', {'books': books})

def return_book(request):
    students = Student.objects.all()
    pupils = Pupil.objects.all()
    users = list(students) + list(pupils)
    users.sort(key=lambda x: x.user_id)

    selected_user = None
    books = []

    if request.method == 'POST':
        user_id = int(request.POST.get('user_id'))
        book_id = request.POST.get('book_id')

        selected_user = Student.objects.filter(user_id=user_id).first() or Pupil.objects.filter(user_id=user_id).first()

        if book_id and selected_user:
            book = selected_user.borrowed_books.filter(id=book_id).first()
            if book:
                selected_user.borrowed_books.remove(book)

                BorrowHistory.objects.create(
                    user_name=f"{selected_user.name} {selected_user.surname}",
                    user_id=selected_user.user_id,
                    book_title=book.title,
                    action='return'
                )

                return redirect('borrowed_books')

        if selected_user:
            books = selected_user.borrowed_books.all()

    return render(request, 'return_book.html', {
        'users': users,
        'selected_user': selected_user,
        'books': books
    })

def borrowed_books_list(request):
    students = Student.objects.prefetch_related('borrowed_books').all()
    pupils = Pupil.objects.prefetch_related('borrowed_books').all()
    users = list(students) + list(pupils)
    users = [u for u in users if u.borrowed_books.exists()]
    users.sort(key=lambda x: x.user_id)
    return render(request, 'borrowed_books.html', {'users': users})

def history(request):
    records = BorrowHistory.objects.all().order_by('-timestamp')
    return render(request, 'history.html', {'records': records})
