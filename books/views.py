from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Book, Category


def book_list(request):
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()

    books = Book.objects.all()

    # 🔍 Search by title, author, or ISBN
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        )

    # 📂 Filter by category if valid
    if category_id.isdigit():
        books = books.filter(category_id=int(category_id))

    # 📄 Paginate results
    paginator = Paginator(books.order_by('-id'), 12)  # Show 12 books per page
    page_number = request.GET.get('page')
    books_page = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'books/book_list.html', {
        'books': books_page,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
    })


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})

