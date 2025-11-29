"""
Setup Google OAuth SocialApplication in the database
Run this after setting CLIENT_ID and CLIENT_SECRET environment variables
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saas_platform.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from decouple import config

# Get credentials from environment
client_id = config('CLIENT_ID', default='')
client_secret = config('CLIENT_SECRET', default='')

if not client_id or not client_secret:
    print("❌ Error: CLIENT_ID and CLIENT_SECRET must be set!")
    print("\nSet them with:")
    print("  export CLIENT_ID=your-client-id")
    print("  export CLIENT_SECRET=your-client-secret")
    print("\nOr add them to a .env file:")
    print("  CLIENT_ID=your-client-id")
    print("  CLIENT_SECRET=your-client-secret")
    exit(1)

# Get the current site
site = Site.objects.get_current()

# Delete any existing Google SocialApps to avoid duplicates
SocialApp.objects.filter(provider='google').delete()

# Create a fresh Google SocialApp
app = SocialApp.objects.create(
    provider='google',
    name='Google',
    client_id=client_id,
    secret=client_secret,
)

# Associate with the current site only
app.sites.set([site])

print(f"✅ Created Google SocialApplication")
print(f"   Client ID: {client_id[:20]}...")
print(f"   Site: {site.domain}")
print(f"   Provider: {app.provider}")
print("\n✅ Google OAuth is now configured!")

