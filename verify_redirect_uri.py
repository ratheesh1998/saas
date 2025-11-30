"""
Verify the redirect URI configuration
This script shows you exactly what redirect URI to add in Google Cloud Console
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saas_platform.settings')
django.setup()

from django.contrib.sites.models import Site
from django.urls import reverse

# Get current site
site = Site.objects.get_current()

# Build the redirect URI
redirect_uri = f"http://{site.domain}/accounts/google/login/callback/"

print("=" * 70)
print("GOOGLE OAUTH REDIRECT URI CONFIGURATION")
print("=" * 70)
print()
print("Your Django application expects this redirect URI:")
print()
print(f"  {redirect_uri}")
print()
print("=" * 70)
print("ACTION REQUIRED:")
print("=" * 70)
print()
print("1. Go to: https://console.cloud.google.com/apis/credentials")
print("2. Click on your OAuth 2.0 Client ID")
print("3. Scroll to 'Authorized redirect URIs'")
print("4. Click '+ ADD URI'")
print("5. Paste this EXACT URI (including trailing slash):")
print()
print(f"   {redirect_uri}")
print()
print("6. Click 'SAVE'")
print("7. Wait 1-2 minutes for changes to propagate")
print()
print("=" * 70)
print("IMPORTANT NOTES:")
print("=" * 70)
print()
print("✓ The URI must match EXACTLY (including trailing slash)")
print("✓ Use 'http://' not 'https://' for localhost")
print("✓ Use 'localhost' not '127.0.0.1' (unless you add both)")
print("✓ Include the port ':8000'")
print()
print("=" * 70)






