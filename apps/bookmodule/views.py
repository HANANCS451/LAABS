from .models import Book
from django.db.models import Q, Avg, Max, Min, Sum, Count
from .models import Address 
from .models import Lab9Book
from django.db.models import  F, FloatField, ExpressionWrapper, Value
from .models import Publisher
from .forms import BookForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Lab9Book, Publisher, Author
from .forms import BookForm # تأكد من إنشاء ملف forms.py أولاً
from datetime import datetime
from .models import Student
from .forms import StudentForm
from .models import Student2
from .forms import Student2Form
from .models import StudentImage
from .forms import ImageForm

def list_images(request):
    images = StudentImage.objects.all()
    return render(request, 'bookmodule/list_images.html', {'images': images})

def upload_image(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('list_images')
    else:
        form = ImageForm()
    return render(request, 'bookmodule/upload_image.html', {'form': form})

def list_students2(request):
    students = Student2.objects.all()
    return render(request, 'bookmodule/list_students2.html', {'students': students})

def add_student2(request):
    if request.method == "POST":
        form = Student2Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_students2') 
    else:
        form = Student2Form()
    return render(request, 'bookmodule/student_form2.html', {'form': form})

def list_students(request):
    students = Student.objects.all()
    return render(request, 'bookmodule/list_students.html', {'students': students})

def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save() # حفظ البيانات في القاعدة
            return redirect('list_students') # العودة التلقائية للقائمة
    else:
        form = StudentForm()
    return render(request, 'bookmodule/student_form.html', {'form': form})

def add_book_form(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save() # يحفظ الكتاب والعلاقات (ManyToMany) تلقائياً
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'bookmodule/book_form.html', {'form': form})

def edit_book_form(request, id):
    book = get_object_or_404(Lab9Book, id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookmodule/book_form.html', {'form': form})

# Task 1: List Books
def list_books2(request):
    books = Lab9Book.objects.all()
    return render(request, 'bookmodule/listbooks.html', {'books': books})
# Task 2: Add Book (Manual)
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        pubdate = request.POST.get('pubdate')
        rating = request.POST.get('rating')
        publisher_id = request.POST.get('publisher')
        
        publisher = Publisher.objects.get(id=publisher_id)
        new_book = Lab9Book.objects.create(
            title=title, price=price, quantity=quantity, 
            pubdate=pubdate, rating=rating, publisher=publisher)
        author_ids = request.POST.getlist('authors')
        new_book.authors.set(author_ids)
        return redirect('list_books')
    publishers = Publisher.objects.all()
    authors = Author.objects.all()
    return render(request, 'bookmodule/addbook.html', {'publishers': publishers, 'authors': authors})

# Task 3: Edit Book (Manual)
def edit_book(request, id):
    book = get_object_or_404(Lab9Book, id=id)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.price = request.POST.get('price')
        book.quantity = request.POST.get('quantity')
        book.rating = request.POST.get('rating')
        pubdate_str = request.POST.get('pubdate')
        if pubdate_str:
            book.pubdate = datetime.fromisoformat(pubdate_str)
        publisher_id = request.POST.get('publisher')
        book.publisher = Publisher.objects.get(id=publisher_id)
        book.save()
        authors_ids = request.POST.getlist('authors')
        book.authors.set(authors_ids)
        return redirect('list_books') # العودة للقائمة[cite: 3]
    publishers = Publisher.objects.all()
    authors = Author.objects.all()
    return render(request, 'bookmodule/edit_book.html', {
        'book': book,
        'publishers': publishers,
        'authors': authors  })

def delete_book(request, id):
    book = get_object_or_404(Lab9Book, id=id)
    book.delete()
    return redirect('list_books')

def task66(request):
    publishers = Publisher.objects.annotate(
        total_filtered_books=Count(
            'lab9book', 
            filter=Q(lab9book__price__gt=50) & 
                   Q(lab9book__quantity__lt=5) & 
                   Q(lab9book__quantity__gte=1)
        )
    )
    return render(request, 'bookmodule/lab9task6.html', {'publishers': publishers})


def task55(request):
    publishers = Publisher.objects.all()
    
    for pub in publishers:
        pub.highly_rated_books = Lab9Book.objects.filter(publisher=pub, rating__gte=4)
    
    return render(request, 'bookmodule/lab9task5.html', {'publishers': publishers})

def task44(request):
    publishers = Publisher.objects.annotate(
        avg_p=Avg('lab9book__price'), 
        min_p=Min('lab9book__price'), 
        max_p=Max('lab9book__price')
    )
    return render(request, 'bookmodule/lab9task4.html', {'publishers': publishers})

from django.db.models import Min, OuterRef, Subquery
from .models import Lab9Book, Publisher

def task33(request):
    oldest_book_name_subquery = Lab9Book.objects.filter(
        publisher=OuterRef('pk')
    ).order_by('pubdate').values('title')[:1]

    publishers = Publisher.objects.annotate(
        oldest_pub_date=Min('lab9book__pubdate'),
        oldest_book_title=Subquery(oldest_book_name_subquery)
    )
    
    return render(request, 'bookmodule/lab9task3.html', {'publishers': publishers})

def task22(request):
    publishers = Publisher.objects.annotate(
        total_stock=Sum('lab9book__quantity')
    )
    
    return render(request, 'bookmodule/lab9task2.html', {'publishers': publishers})

def task11(request):
    total_books = Lab9Book.objects.aggregate(total=Sum('quantity'))['total'] or 0

    if total_books == 0:
        books = Lab9Book.objects.annotate(
            availability_percentage=Value(0.0, output_field=FloatField())
        )
    else:
        books = Lab9Book.objects.annotate(
            availability_percentage=ExpressionWrapper(
                (F('quantity') * 100.0) / total_books,
                output_field=FloatField()
            )
        )

    return render(request, 'bookmodule/lab9task1.html', {'books': books})

def task7(request):
     cities = Address.objects.annotate(student_count=Count('student'))
     return render(request, 'bookmodule/task7.html', {'cities': cities})
def task5(request):
    stats = Book.objects.aggregate(
        total_books=Count('id'),      
        total_price=Sum('price'),     
        average_price=Avg('price'),   
        maximum_price=Max('price'),   
        minimum_price=Min('price')    
    )
    return render(request, 'bookmodule/task5.html', {'stats': stats})

def task4(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'bookmodule/task4.html', {'books': books})

def task3(request):
    books = Book.objects.filter(
        ~Q(edition__gt=3) & ~(Q(title__icontains='qu') | Q(author__icontains='qu'))
    )
    return render(request, 'bookmodule/task3.html', {'books': books})

def task2(request):
    books = Book.objects.filter(
        Q(edition__gt=3) & (Q(title__icontains='qu') | Q(author__icontains='qu'))
    )
    return render(request, 'bookmodule/task2.html', {'books': books})

def task1(request):
    books = Book.objects.filter(Q(price__lte=80))
    return render(request, 'bookmodule/task1.html', {'books': books})

def simple_query(request):
    mybooks=Book.objects.filter(title__icontains='and') # <- multiple objects
    return render(request, 'bookmodule/bookList.html', {'books':mybooks})

def complex_query(request):
    mybooks = Book.objects.filter(
        author__isnull=False
    ).filter(
        title__icontains='and'
    ).filter(
        edition__gte=2
    ).exclude(
        price__lte=100
    )[:10]

    if mybooks.exists():
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})
    else:
        return render(request, 'bookmodule/index.html')
def index(request):
    return render(request, "bookmodule/index.html")

def list_books(request):
    return render(request, "bookmodule/list_books.html")

def viewbook(request, bookId):
    return render(request, "bookmodule/one_book.html")

def aboutus(request):
    return render(request, "bookmodule/aboutus.html")
def links(request):
    return render(request,'bookmodule/links.html')

def formatting(request):
    return render(request,'bookmodule/formatting.html')

def listing(request):
    return render(request,'bookmodule/listing.html')

def tables(request):
    return render(request,'bookmodule/tables.html')


def __getBooksList():
    book1 = {'id': 12344321, 'title': 'Continuous Delivery', 'author': 'J.Humble and D. Farley'}
    book2 = {'id': 56788765, 'title': 'Reversing: Secrets of Reverse Engineering', 'author': 'E. Eilam'}
    book3 = {'id': 43211234, 'title': 'The Hundred-Page Machine Learning Book', 'author': 'Andriy Burkov'}
    return [book1, book2, book3]


def search(request):
    if request.method == "POST":
        string = request.POST.get('keyword', '').lower().strip()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')

        books = __getBooksList()
        newBooks = []

        for item in books:
            contained = False
            if isTitle and string in item['title'].lower():
                contained = True
            if not contained and isAuthor and string in item['author'].lower():
                contained = True

            if contained:
                newBooks.append(item)

        return render(request, 'bookmodule/bookList.html', {'books': newBooks})

    return render(request, 'bookmodule/search.html')