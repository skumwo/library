from django.contrib import admin
from .models import Book, Student, Pupil

admin.site.register(Book)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'surname', 'group')
    readonly_fields = ('user_id',)
    exclude = ('borrowed_books',)


@admin.register(Pupil)
class PupilAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'surname', 'group', 'age')
    readonly_fields = ('user_id',)
    exclude = ('borrowed_books',)
