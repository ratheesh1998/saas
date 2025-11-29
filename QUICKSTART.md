# Quick Start Guide

## Initial Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   export SECRET_KEY=your-secret-key-here
   export DEBUG=True
   export CLIENT_ID=your-google-client-id
   export CLIENT_SECRET=your-google-client-secret
   ```
   Or create a `.env` file and load it using a tool like `python-decouple` or `python-dotenv`.

3. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the server:**
   ```bash
   python manage.py runserver
   ```

6. **Visit the application:**
   Open your browser and go to `http://localhost:8000`

## Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI: `http://localhost:8000/accounts/google/login/callback/`
6. Set `CLIENT_ID` and `CLIENT_SECRET` as environment variables

## Features

- ✅ User registration with email
- ✅ User login
- ✅ Google OAuth authentication
- ✅ HTMX-powered SPA (no page reloads)
- ✅ Responsive, minimal design
- ✅ Dashboard for authenticated users

## Testing the HTMX Features

1. Click "Login" or "Sign Up" in the navigation - the form loads without page reload
2. Submit the form - it processes via HTMX without reloading
3. Navigate between pages - smooth transitions without full page reloads

## Next Steps

You can now add:
- Product deployment features
- User management
- Billing system
- API endpoints
- And more...

