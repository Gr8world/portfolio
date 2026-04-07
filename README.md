# TechNova - IT Startup Landing Page

A production-ready Django landing page for a modern IT startup company.

## Features

- **Modern UI**: Responsive design with Tailwind CSS
- **Sections**: Hero, Services, About, Portfolio, Testimonials, Pricing, Contact, Footer
- **CMS**: Django Admin for content management
- **Contact Form**: Stores messages in database, viewable in admin
- **SEO Optimized**: Meta tags, fast loading structure
- **Error Pages**: Custom 404 and 500 pages

## Tech Stack

- Django 4.2+
- Tailwind CSS (via CDN)
- Font Awesome Icons
- AOS Animation Library
- SQLite (default) / PostgreSQL ready

## Quick Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Create environment file** (optional):
```bash
cp .env.example .env
```

3. **Run migrations**:
```bash
python manage.py migrate
```

4. **Create admin user**:
```bash
python manage.py createsuperuser
```

5. **Run server**:
```bash
python manage.py runserver
```

6. **Visit**: http://127.0.0.1:8000

## Admin Panel

- URL: http://127.0.0.1:8000/admin
- Manage: Services, Projects, Testimonials, Pricing Plans, Contact Messages

## Project Structure

```
startup_site/
├── core/               # Main Django app
│   ├── models.py       # Database models
│   ├── views.py        # Views
│   ├── admin.py        # Admin configuration
│   └── urls.py         # App URLs
├── templates/           # HTML templates
│   └── core/
│       ├── base.html
│       ├── home.html
│       └── includes/
├── static/             # CSS, JS, Images
├── startup_site/       # Django project
│   ├── settings.py
│   └── urls.py
├── media/              # User uploads
├── requirements.txt
└── manage.py
```

## Configuration

### Environment Variables (.env)

```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=django.db.backends.sqlite3
```

### PostgreSQL Setup

Set these in your environment for PostgreSQL:
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=startup_site
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

## License

MIT License