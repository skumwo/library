from django.contrib import admin
from django.urls import path
from library import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('register/', views.register_user, name='register_user'),
    path('users/', views.user_list, name='user_list'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/', views.book_list, name='book_list'),
    path('assign/', views.assign_book, name='assign_book'),
    path('return/', views.return_book, name='return_book'),
    path('borrowed/', views.borrowed_books_list, name='borrowed_books'),
    path('return_one/', views.return_single_book, name='return_one'),
    path('books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('history/', views.history, name='history'),

]

