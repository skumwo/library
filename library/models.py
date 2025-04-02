from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, unique=True)
    year = models.IntegerField()
    quantity = models.IntegerField()
    label = models.CharField(max_length=50, choices=[("for children", "For children"), ("general", "General")])

    def __str__(self):
        return f"{self.title} ({self.label})"


class User(models.Model):
    user_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    group = models.CharField(max_length=50)
    borrowed_books = models.ManyToManyField(Book, blank=True)

    class Meta:
        abstract = True

    def identify_type(self):
        if str(self.user_id).startswith("2"):
            return "This is a student"
        elif str(self.user_id).startswith("1"):
            return "This is a pupil"
        return "Unknown type"

    def can_borrow(self, book):
        raise NotImplementedError


class Student(User):
    def can_borrow(self, book):
        return True


class Pupil(User):
    age = models.PositiveIntegerField()

    def can_borrow(self, book):
        if self.age < 7:
            return False
        return book.label == "for children"

class BorrowHistory(models.Model):
    ACTION_CHOICES = [('borrow', 'Borrow'), ('return', 'Return')]

    user_name = models.CharField(max_length=200)
    user_id = models.PositiveIntegerField()
    book_title = models.CharField(max_length=255)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} {self.action} '{self.book_title}' on {self.timestamp}"