# 🚀 SaaS Platform

> **Build Your Own SaaS Business — Platform is Free, Powered by Railway API**

A powerful, open-source platform that enables you to create, deploy, and manage cloud-based projects as a service. Whether you're a solo entrepreneur or a growing business, this platform gives you the foundation to launch your own SaaS business.

> 📢 **Note:** This platform is free to use. It integrates with [Railway API](https://railway.app/) for cloud deployments, which is a paid third-party service.

---

## 🎯 What Is This?

**SaaS Platform** is a free, open-source Django + HTMX application designed to help you:

- 🏗️ **Create Cloud Projects** — Build and deploy your own cloud-based applications
- 💼 **Launch Your SaaS Business** — Turn your ideas into subscription-based services
- 🌐 **Offer as a Service** — Let your customers access powerful tools through your platform
- 💰 **Free Platform** — This project is completely free to use, modify, and deploy
- 🚂 **Powered by Railway** — Uses Railway API for reliable cloud infrastructure (Railway is a paid service)

This project empowers developers, startups, and businesses to enter the SaaS market with a solid, production-ready foundation.

---

## 🚧 Project Status

> ⚠️ **Currently Under Active Development**

This project is being actively built and improved. New features are added regularly. Feel free to:
- Star ⭐ the repo to follow progress
- Contribute with PRs and ideas
- Report issues and suggestions
- Use it for your own projects (it's free!)

---

## ✨ Features

| Feature | Status |
|---------|--------|
| User Registration & Login | ✅ Ready |
| Google OAuth Authentication | ✅ Ready |
| HTMX-powered SPA Experience | ✅ Ready |
| Modern, Responsive UI | ✅ Ready |
| Railway API Integration | 🔨 In Progress |
| Project Management | 🔨 In Progress |
| Template Editor | 🔨 In Progress |
| Service Deployment via Railway | 🔨 In Progress |
| Multi-tenant Support | 📋 Planned |
| Billing & Subscriptions | 📋 Planned |
| API Endpoints | 📋 Planned |
| Railway Deployment Ready | ✅ Ready |

---

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **Django 5.0** | Backend Web Framework |
| **HTMX** | Dynamic SPA-like Experience (No Page Reloads) |
| **django-allauth** | Authentication (Google OAuth included) |
| **Bootstrap 5** | Modern UI Components |
| **Crispy Forms** | Beautiful Form Styling |
| **Railway API** | Cloud Deployment & Infrastructure |

---

## 💳 Important: Railway API (Paid Service)

> ⚠️ **Please Note: This platform uses the Railway API for cloud deployments**

This project integrates with [Railway](https://railway.app/) to provide cloud infrastructure and deployment capabilities. While **this SaaS Platform project itself is completely free**, Railway is a **paid third-party service**.

### What You Need to Know:

| Aspect | Details |
|--------|---------|
| **This Project** | ✅ Free & Open Source |
| **Railway API** | 💳 Paid Service (usage-based pricing) |
| **Railway Account** | Required for deployment features |
| **Railway API Token** | Needed to connect your deployments |

### Railway Pricing:

- Railway offers a **free trial** with limited credits
- After trial, you pay based on resource usage (compute, memory, bandwidth)
- Check [Railway Pricing](https://railway.app/pricing) for current rates

### Why Railway?

- 🚀 Seamless deployment from GitHub
- 🔧 Easy environment management
- 📊 Built-in monitoring and logs
- 🌐 Automatic SSL and custom domains
- ⚡ Fast, reliable infrastructure

**Bottom Line:** The platform code is free — you only pay Railway for the cloud resources you use when deploying projects.

---

## 🚀 Quick Start

### 1. Clone & Setup Environment

```bash
git clone https://github.com/your-username/saas-platform.git
cd saas-platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Set the following environment variables (or create a `.env` file):

```bash
export SECRET_KEY=your-secret-key-here
export DEBUG=True
export ALLOWED_HOSTS=localhost,127.0.0.1
export CLIENT_ID=your-google-client-id
export CLIENT_SECRET=your-google-client-secret
```

### 4. Google OAuth Setup (Optional)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable Google+ API
3. Create OAuth 2.0 credentials
4. Add redirect URI: `http://localhost:8000/accounts/google/login/callback/`
5. Set `CLIENT_ID` and `CLIENT_SECRET` environment variables

See `GOOGLE_OAUTH_SETUP.md` for detailed instructions.

### 5. Initialize Database

```bash
python manage.py makemigrations
python manage.py migrate
python setup_google_oauth.py  # Optional: Setup Google OAuth
```

### 6. Run the Server

```bash
python manage.py runserver
```

🎉 Visit `http://localhost:8000` to see your platform!

---

## 📁 Project Structure

```
saas_platform/
├── accounts/          # User auth, profiles, settings
├── core/              # Main app (home, dashboard, projects)
├── saas_platform/     # Django settings & config
├── templates/         # HTMX-powered HTML templates
├── static/            # CSS, JS, images
└── manage.py
```

---

## 🌍 Deployment

This project uses the **Railway API** for cloud deployments:

### Setup Railway Integration:

1. Create an account at [Railway](https://railway.app/)
2. Generate an API token from your Railway dashboard
3. Add your Railway API token to environment variables:
   ```bash
   export RAILWAY_API_TOKEN=your-railway-api-token
   ```
4. Connect your projects and deploy through the platform

### Direct Railway Deployment:

You can also deploy this platform itself on Railway:

1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy! Railway handles the rest

> 💡 **Remember:** Railway is a paid service. Monitor your usage to manage costs.

---

## 🤝 Contributing

Contributions are welcome! This is a community-driven project, and we'd love your help to make it even better.

- 🐛 Report bugs via Issues
- 💡 Suggest features
- 🔧 Submit Pull Requests
- 📖 Improve documentation

---

## 📜 License

This project is **free and open-source**. Use it for personal or commercial purposes.

---

## 💬 Support

Have questions? Need help?

- Open an Issue on GitHub
- Check the `QUICKSTART.md` for quick reference
- Review `GOOGLE_OAUTH_SETUP.md` for OAuth setup

---

<div align="center">

**Built with ❤️ for the SaaS Community**

*Empowering everyone to build their own cloud business*

⭐ Star this repo if you find it useful!

</div>
