# scripts/convert_pdfs_to_zip.py
import os
import zipfile
from django.core.files import File
from django.core.management.base import BaseCommand
from main.models import Book
from django.conf import settings
import tempfile
import shutil

class Command(BaseCommand):
    help = 'Convert PDF files to ZIP archives containing the PDF'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Perform a dry run without making actual changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        books = Book.objects.exclude(pdf_file='')
        total_books = books.count()
        
        self.stdout.write(f"Found {total_books} books with PDF files")
        
        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN - No changes will be made"))
        
        converted_count = 0
        error_count = 0
        
        for book in books:
            try:
                self.convert_pdf_to_zip(book, dry_run)
                converted_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully converted: {book.pdf_file.name}")
                )
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f"Error converting {book.pdf_file.name}: {str(e)}")
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Conversion complete. Converted: {converted_count}, Errors: {error_count}"
            )
        )
    
    def convert_pdf_to_zip(self, book, dry_run=False):
        """Convert a single book's PDF to ZIP archive"""
        
        # Get the path to the original PDF
        pdf_path = book.pdf_file.path
        
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create zip file path in temp directory
            zip_filename = os.path.splitext(os.path.basename(pdf_path))[0] + '.zip'
            zip_path = os.path.join(temp_dir, zip_filename)
            
            # Create zip archive with the PDF
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add PDF to zip with just the filename (not full path)
                zipf.write(pdf_path, arcname=os.path.basename(pdf_path))
            
            if not dry_run:
                # Store the original PDF path for deletion after successful upload
                old_pdf_path = pdf_path
                
                # Open the zip file and save it to the model
                with open(zip_path, 'rb') as zip_file:
                    # Save the new zip file
                    book.pdf_file.save(zip_filename, File(zip_file), save=True)
                
                # Delete the original PDF file
                if os.path.exists(old_pdf_path):
                    os.remove(old_pdf_path)
                
                self.stdout.write(f"Converted: {book.pdf_file.name}")
            else:
                self.stdout.write(f"[DRY RUN] Would convert: {book.pdf_file.name}")

