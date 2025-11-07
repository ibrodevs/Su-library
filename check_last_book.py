#!/usr/bin/env python
"""Check last uploaded book"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from main.models import Book

try:
    book = Book.objects.last()
    if book:
        print(f"Book ID: {book.id}")
        print(f"Year: {book.year}")
        print(f"Active: {book.is_active}")
        print()
        if book.pdf_file:
            print(f"PDF path: {book.pdf_file.name}")
            print(f"PDF URL: {book.pdf_file.url}")
        else:
            print("No PDF file")
        print()
        if book.cover_image:
            print(f"Cover path: {book.cover_image.name}")
            print(f"Cover URL: {book.cover_image.url}")
        else:
            print("No cover image")
    else:
        print("No books found")
except Exception as e:
    print(f"Error: {e}")
