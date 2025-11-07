#!/usr/bin/env python
"""Create a superuser for Heroku deployment"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create superuser if it doesn't exist
username = 'admin'
email = 'admin@su-library.com'
password = 'Admin123456'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'✅ Superuser "{username}" created successfully!')
    print(f'   Email: {email}')
    print(f'   Password: {password}')
else:
    print(f'ℹ️  Superuser "{username}" already exists')
