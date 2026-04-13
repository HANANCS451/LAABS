from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="books.index"),
    path('list_books/', views.list_books, name="books.list_books"),
    path('<int:bookId>/', views.viewbook, name="books.view_one_book"),
    path('aboutus/', views.aboutus, name="books.aboutus"),
    path('html5/links', views.links),
    path('html5/text/formatting', views.formatting),
    path('html5/listing', views.listing),
    path('html5/tables', views.tables),
    path('search/', views.search, name='books.search'),
    path('simple/query', views.simple_query, name='books.simple_query'),
    path('complex/query', views.complex_query, name='books.complex_query'),
    path('task1', views.task1, name='task1'),
    path('task2', views.task2, name='task2'),
    path('task3', views.task3, name='task3'),
    path('task4', views.task4, name='task4'),
    path('task5', views.task5, name='task5'),
    path('task7', views.task7, name='task7'),


]
