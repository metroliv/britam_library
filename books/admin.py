from django.contrib import admin
from .models import Book, Category

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'isbn', 'category', 'available_copies')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('category', 'publication_year')

admin.site.register(Category)
