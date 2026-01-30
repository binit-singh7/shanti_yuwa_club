# Shanti Yuwa Club Website

A modern, responsive website for Shanti Yuwa Club - a youth-led community organization in Biratnagar, Nepal.

## Features

- 🎨 Modern, responsive design with Tailwind CSS
- 📱 Mobile-friendly interface
- 👥 Member registration and management
- 📋 Program enrollment system
- 🖼️ Photo gallery with categories
- 📧 Contact form with email notifications
- 🔐 Secure admin panel
- 🌐 Production-ready deployment configuration

## Tech Stack

- **Backend:** Django 5.2.4
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **Database:** PostgreSQL (production) / SQLite (development)
- **Deployment:** Render.com
- **Static Files:** WhiteNoise

## Local Development Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/shanti_yuwa_club.git
   cd shanti_yuwa_club
   ```

2. **Create virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations:**

   ```bash
   python manage.py migrate
   ```

6. **Create superuser:**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server:**

   ```bash
   python manage.py runserver
   ```

8. **Visit:** http://localhost:8000

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on deploying to Render.com.

**Quick summary:**

1. Push code to GitHub
2. Create Render account
3. Create PostgreSQL database
4. Create web service
5. Set environment variables
6. Deploy!

**Live Site:** https://shanti-yuwa-club.onrender.com

## Environment Variables

Required environment variables (see `.env.example`):

- `DJANGO_SECRET_KEY` - Django secret key
- `DJANGO_DEBUG` - Debug mode (True/False)
- `DATABASE_URL` - PostgreSQL connection string
- `EMAIL_HOST_USER` - Email address for sending
- `EMAIL_HOST_PASSWORD` - Email app password
- `ALLOWED_HOSTS` - Comma-separated allowed hosts

## Project Structure

```
shanti_yuwa_club/
├── main/                   # Main Django app
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── forms.py           # Form definitions
│   └── admin.py           # Admin configuration
├── shanti_yuwa_club/      # Project settings
│   ├── settings.py        # Development settings
│   ├── settings_prod.py   # Production settings
│   └── urls.py            # URL configuration
├── templates/             # HTML templates
├── static/               # Static files (CSS, JS, images)
├── media/                # User-uploaded files
├── requirements.txt      # Python dependencies
├── Procfile             # Render deployment config
├── build.sh             # Build script
└── DEPLOYMENT.md        # Deployment guide
```

## Admin Panel

Access the admin panel at `/admin` with superuser credentials.

**Features:**

- Member management
- Program management
- Gallery management
- Team member profiles
- Contact form submissions

## Backup & Maintenance

**Backup database:**

```bash
./backup_db.sh
```

**View logs (on Render):**
Go to Dashboard → Your Service → Logs

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Shanti Yuwa Club  
Email: shantiyuwac@gmail.com  
Location: Biratnagar, Nepal

---

**Made with ❤️ by Shanti Yuwa Club**
