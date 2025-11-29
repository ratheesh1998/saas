# Google OAuth Redirect URI Setup Guide

## Current Configuration

Your Django application is configured to use this redirect URI:
```
http://localhost:8000/accounts/google/login/callback/
```

## Steps to Fix Redirect URI Mismatch

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Select your project

2. **Navigate to OAuth 2.0 Credentials**
   - Go to **APIs & Services** → **Credentials**
   - Find your OAuth 2.0 Client ID (the one matching your `CLIENT_ID`)
   - Click on it to edit

3. **Add Authorized Redirect URIs**
   - Scroll down to **Authorized redirect URIs**
   - Click **+ ADD URI**
   - Add this **exact** URI (copy and paste to avoid typos):
     ```
     http://localhost:8000/accounts/google/login/callback/
     ```
   - **Important**: The URI must match exactly:
     - ✅ Protocol: `http://` (not `https://` for localhost)
     - ✅ Domain: `localhost` (not `127.0.0.1`)
     - ✅ Port: `:8000`
     - ✅ Path: `/accounts/google/login/callback/`
     - ✅ Trailing slash: Must include the trailing `/`

4. **Save Changes**
   - Click **SAVE** at the bottom of the page
   - Wait a few seconds for changes to propagate

5. **Test Again**
   - Try the Google login button again
   - If it still doesn't work, wait 1-2 minutes for Google's servers to update

## Common Issues

### Issue: "redirect_uri_mismatch" error
**Solution**: Make sure the URI in Google Cloud Console matches exactly:
- Check for typos
- Ensure trailing slash is present
- Verify `http://` (not `https://`) for localhost
- Make sure port `:8000` is included

### Issue: Multiple redirect URIs
You can add multiple redirect URIs if needed:
- `http://localhost:8000/accounts/google/login/callback/`
- `http://127.0.0.1:8000/accounts/google/login/callback/` (if you access via IP)

### Issue: Still not working after adding URI
1. Clear your browser cache
2. Wait 2-3 minutes for Google's changes to propagate
3. Make sure you're using the correct OAuth Client ID (check your `CLIENT_ID` environment variable)

## Verification

After adding the redirect URI, you can verify it's correct by:
1. Going to Google Cloud Console → Credentials
2. Clicking on your OAuth 2.0 Client ID
3. Checking that `http://localhost:8000/accounts/google/login/callback/` appears in the **Authorized redirect URIs** list

## Production Setup

When deploying to production, you'll need to:
1. Add your production redirect URI (e.g., `https://yourdomain.com/accounts/google/login/callback/`)
2. Update the Site domain in Django admin or via `setup_google_oauth.py`
3. Ensure your production domain matches the Site configuration




