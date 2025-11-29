"""
Fix duplicate Google SocialApplications
Removes duplicates and keeps only one with the correct credentials
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
    exit(1)

# Get all Google SocialApps
google_apps = SocialApp.objects.filter(provider='google')
print(f"Found {google_apps.count()} Google SocialApplication(s)")

# Delete all existing Google apps
if google_apps.exists():
    count = google_apps.count()
    google_apps.delete()
    print(f"✅ Deleted {count} existing Google SocialApplication(s)")

# Get the current site
site = Site.objects.get_current()

# Create a fresh Google SocialApp
app = SocialApp.objects.create(
    provider='google',
    name='Google',
    client_id=client_id,
    secret=client_secret,
)

# Associate with the current site
app.sites.add(site)

print(f"✅ Created new Google SocialApplication")
print(f"   Client ID: {client_id[:20]}...")
print(f"   Site: {site.domain}")
print(f"   Provider: {app.provider}")
print("\n✅ Google OAuth is now properly configured!")




