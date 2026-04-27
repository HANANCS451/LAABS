from django.shortcuts import render
from .models import Book
from django.db.models import Q
from django.db.models import Q, Avg, Max, Min, Sum, Count
from .models import Address 
from .models import Lab9Book
from django.db.models import  F, FloatField, ExpressionWrapper, Value
from .models import Publisher

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