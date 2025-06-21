from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from books.models import Book
from members.models import MemberProfile
from borrowing.models import BorrowRecord
from django.contrib.auth.models import User
from datetime import date

@login_required
def home(request):
    total_books = Book.objects.count()
    total_members = User.objects.count()
    total_borrowed = BorrowRecord.objects.filter(return_date__isnull=True).count()
    total_returned = BorrowRecord.objects.filter(return_date__isnull=False).count()
    overdue_books = BorrowRecord.objects.filter(return_date__isnull=True, due_date__lt=date.today()).count()

    context = {
        'total_books': total_books,
        'total_members': total_members,
        'total_borrowed': total_borrowed,
        'total_returned': total_returned,
        'overdue_books': overdue_books,
    }
    return render(request, 'dashboard/home.html', context)
