# SaaS Platform

A Django-based platform for deploying and managing SaaS products. Built with HTMX for a single-page application experience without page reloads.

## Features

- ✅ User Registration & Login
- ✅ Google OAuth Authentication
- ✅ HTMX-powered SPA-like experience (no page reloads)
- ✅ Minimal and attractive UI design
- ✅ Responsive design

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Set environment variables:

```bash
export SECRET_KEY=your-secret-key-here
export DEBUG=True
export ALLOWED_HOSTS=localhost,127.0.0.1
export CLIENT_ID=your-google-client-id
export CLIENT_SECRET=your-google-client-secret
```

Or create a `.env` file and load it, or set them in your system environment.

### 4. Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable Google+ API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. **IMPORTANT**: Add authorized redirect URI: `http://localhost:8000/accounts/google/login/callback/`
   - The URI must match **exactly** (including trailing slash)
   - See `GOOGLE_OAUTH_SETUP.md` for detailed instructions
   - Run `python verify_redirect_uri.py` to see the exact URI needed
6. Set `CLIENT_ID` and `CLIENT_SECRET` as environment variables

### 5. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Setup Google OAuth

After setting your `CLIENT_ID` and `CLIENT_SECRET` environment variables, run:

```bash
python setup_google_oauth.py
```

This will create the Google OAuth SocialApplication in the database.

### 7. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 8. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to see the application.

## Project Structure

```
saas_platform/
├── accounts/          # User authentication app
├── core/              # Main app (home, dashboard)
├── saas_platform/     # Project settings
├── templates/        # HTML templates
├── static/           # CSS, JS, images
└── manage.py
```

## Technology Stack

- **Django 5.0** - Web framework
- **django-allauth** - Authentication (including Google OAuth)
- **HTMX** - Dynamic content without page reloads
- **Bootstrap 5** - UI framework
- **Crispy Forms** - Form styling

## Next Steps

This is the initial setup. You can now add:
- Product deployment features
- User management
- Billing/subscription system
- API endpoints
- And more...
