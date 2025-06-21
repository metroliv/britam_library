from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    publication_year = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    
    # ✅ New Fields
    description = models.TextField(blank=True, null=True)
    page_count = models.PositiveIntegerField(blank=True, null=True)
    publisher = models.CharField(max_length=200, blank=True, null=True)
    preview_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} by {self.author}"
