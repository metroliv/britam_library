import os
import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from books.models import Book, Category

class Command(BaseCommand):
    help = 'Import 10,000+ books from Google Books API with full details and cover images'

    def handle(self, *args, **kwargs):
        topics = [
            "science", "technology", "engineering", "mathematics", "fiction",
            "non-fiction", "history", "philosophy", "medicine", "programming",
            "education", "economics", "biography", "travel", "art", "design",
            "law", "psychology", "astronomy", "AI", "machine learning", "sports"
        ]

        total_imported = 0

        for topic in topics:
            self.stdout.write(self.style.WARNING(f"\n🔎 Fetching books on topic: {topic}"))

            for start in range(0, 1000, 40):  # Google API: max 1000 per topic
                url = f"https://www.googleapis.com/books/v1/volumes?q={topic}&startIndex={start}&maxResults=40"
                response = requests.get(url)

                if response.status_code != 200:
                    self.stdout.write(self.style.ERROR(f"❌ Failed at start={start} for topic: {topic}"))
                    break

                items = response.json().get("items", [])
                if not items:
                    break

                for item in items:
                    info = item.get('volumeInfo', {})
                    title = info.get('title', 'Untitled')
                    authors = ", ".join(info.get('authors', ['Unknown']))
                    isbn_list = info.get('industryIdentifiers', [])
                    isbn = isbn_list[0]['identifier'] if isbn_list else f"{topic[:3]}-{start}"

                    published_year = info.get('publishedDate', '2000')[:4]
                    try:
                        year = int(published_year)
                    except ValueError:
                        year = 2000

                    category_name = info.get('categories', ['General'])[0]
                    category, _ = Category.objects.get_or_create(name=category_name)

                    # NEW: Extended fields
                    description = info.get('description', '')
                    page_count = info.get('pageCount', 0)
                    publisher = info.get('publisher', 'Unknown')
                    preview_link = info.get('previewLink', '')

                    if not Book.objects.filter(isbn=isbn).exists():
                        book = Book.objects.create(
                            title=title,
                            author=authors,
                            isbn=isbn,
                            publication_year=year,
                            category=category,
                            total_copies=5,
                            available_copies=5,
                            description=description,
                            page_count=page_count,
                            publisher=publisher,
                            preview_link=preview_link
                        )

                        # ✅ Download and save cover image
                        image_links = info.get('imageLinks', {})
                        thumbnail_url = image_links.get('thumbnail')
                        if thumbnail_url:
                            try:
                                image_response = requests.get(thumbnail_url)
                                if image_response.status_code == 200:
                                    img_name = f"{isbn}.jpg"
                                    book.cover_image.save(img_name, ContentFile(image_response.content), save=True)
                            except Exception:
                                self.stdout.write(self.style.WARNING(f"⚠️ Failed to download image for {title}"))

                        total_imported += 1
                        self.stdout.write(self.style.SUCCESS(f"✔ Imported: {title}"))

        self.stdout.write(self.style.SUCCESS(f"\n✅ Total books imported: {total_imported}"))
