"""
Quick setup script for the SaaS Platform
Run this after installing dependencies to set up the database
"""
import os
import sys
import django

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saas_platform.settings')
    django.setup()
    
    from django.core.management import execute_from_command_line
    
    print("Setting up SaaS Platform...")
    print("1. Making migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    print("2. Running migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Create a .env file with your configuration (see .env.example)")
    print("2. Set up Google OAuth credentials (see README.md)")
    print("3. Run: python manage.py runserver")
    print("4. Visit: http://localhost:8000")

