from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import timedelta, date

from books.models import Book
from .models import BorrowRecord
from django.contrib.admin.views.decorators import staff_member_required

@login_required
def borrow_dashboard(request):
    books = Book.objects.all()
    return render(request, 'borrowing/borrow_dashboard.html', {'books': books})

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # Check if user already borrowed this book and has not returned it
    existing = BorrowRecord.objects.filter(user=request.user, book=book, return_date__isnull=True).exists()
    if existing:
        messages.warning(request, f"You've already borrowed '{book.title}' and haven't returned it yet.")
        return redirect('borrow_dashboard')

    if book.available_copies > 0:
        BorrowRecord.objects.create(
            user=request.user,
            book=book,
            due_date=date.today() + timedelta(days=14)
        )
        book.available_copies -= 1
        book.save()
        messages.success(request, f"You successfully borrowed '{book.title}'. Due in 14 days.")
        return redirect('borrow_history')
    else:
        messages.error(request, f"'{book.title}' is currently unavailable.")
        return render(request, 'borrowing/unavailable.html', {'book': book})

@login_required
def return_book(request, record_id):
    record = get_object_or_404(BorrowRecord, id=record_id, user=request.user)

    if not record.return_date:
        record.return_date = date.today()
        record.book.available_copies += 1
        record.book.save()
        record.save()
        messages.success(request, f"You successfully returned '{record.book.title}'.")
    else:
        messages.warning(request, f"'{record.book.title}' was already returned.")

    return redirect('borrow_history')

@login_required
def borrow_history(request):
    records = BorrowRecord.objects.filter(user=request.user).order_by('-borrow_date')
    return render(request, 'borrowing/history.html', {'records': records})

@staff_member_required
def all_borrow_records(request):
    all_records = BorrowRecord.objects.all().order_by('-borrow_date')
    return render(request, 'borrowing/all_records.html', {'records': all_records})