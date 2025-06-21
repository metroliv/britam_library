from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from datetime import timedelta, date

class BorrowRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def is_overdue(self):
        return self.return_date is None and date.today() > self.due_date

    def status(self):
        if self.return_date:
            return 'Returned'
        elif self.is_overdue():
            return 'Overdue'
        else:
            return 'Borrowed'

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
