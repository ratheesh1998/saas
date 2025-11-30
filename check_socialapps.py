"""
Check SocialApplications in the database
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saas_platform.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

# Get all Google apps
google_apps = SocialApp.objects.filter(provider='google')
print(f"Total Google SocialApps: {google_apps.count()}")

for app in google_apps:
    site_ids = list(app.sites.values_list('id', flat=True))
    print(f"  App ID {app.id}:")
    print(f"    Name: {app.name}")
    print(f"    Client ID: {app.client_id[:20]}...")
    print(f"    Sites: {site_ids}")

current_site = Site.objects.get_current()
print(f"\nCurrent site ID: {current_site.id}, Domain: {current_site.domain}")

if google_apps.count() > 1:
    print("\n⚠️  WARNING: Multiple Google SocialApps found!")
    print("   This will cause MultipleObjectsReturned error.")
    print("   Run: python setup_google_oauth.py to fix this.")
elif google_apps.count() == 1:
    app = google_apps.first()
    if current_site in app.sites.all():
        print("\n✅ Google OAuth is properly configured!")
    else:
        print(f"\n⚠️  WARNING: Google SocialApp is not associated with current site!")
        print(f"   Run: python setup_google_oauth.py to fix this.")
else:
    print("\n❌ No Google SocialApp found!")
    print("   Run: python setup_google_oauth.py to create one.")






