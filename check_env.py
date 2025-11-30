"""
Quick script to check if environment variables are set correctly
"""
import os
from decouple import config

print("Checking environment variables...")
print("-" * 50)

# Check CLIENT_ID
client_id = config('CLIENT_ID', default='')
if client_id:
    print(f"✅ CLIENT_ID is set: {client_id[:20]}...")
else:
    print("❌ CLIENT_ID is NOT set")
    print("   Set it with: export CLIENT_ID=your-client-id")
    print("   Or add it to a .env file: CLIENT_ID=your-client-id")

# Check CLIENT_SECRET
client_secret = config('CLIENT_SECRET', default='')
if client_secret:
    print(f"✅ CLIENT_SECRET is set: {client_secret[:20]}...")
else:
    print("❌ CLIENT_SECRET is NOT set")
    print("   Set it with: export CLIENT_SECRET=your-client-secret")
    print("   Or add it to a .env file: CLIENT_SECRET=your-client-secret")

# Check SECRET_KEY
secret_key = config('SECRET_KEY', default='')
if secret_key and secret_key != 'django-insecure-change-this-in-production':
    print("✅ SECRET_KEY is set")
else:
    print("⚠️  SECRET_KEY is using default value (not recommended for production)")

print("-" * 50)

if not client_id or not client_secret:
    print("\n⚠️  Google OAuth will not work until CLIENT_ID and CLIENT_SECRET are set!")
    print("\nTo set them:")
    print("1. Create a .env file in the project root")
    print("2. Add these lines:")
    print("   CLIENT_ID=your-google-client-id")
    print("   CLIENT_SECRET=your-google-client-secret")
    print("\nOr set them as environment variables before running the server.")
else:
    print("\n✅ All required environment variables are set!")





