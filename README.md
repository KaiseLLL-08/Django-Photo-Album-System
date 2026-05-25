# 📸 PhotoAlbum Management System

A production-ready Django web application for managing photo albums with role-based access control.

## 🔗 Links
- **Live URL**: https://your-app.onrender.com
- **GitHub**: https://github.com/your-username/your-repo

## ✨ Features
- User registration and authentication
- Role-Based Access Control (Standard User & Administrator)
- Create, view, edit, and delete albums
- Upload, view, edit, and delete photos
- Cloudinary cloud storage for all images
- Responsive Bootstrap UI
- PostgreSQL database

## 🛠 Technologies
| Technology | Purpose |
|---|---|
| Django | Web framework |
| Python | Programming language |
| PostgreSQL | Database |
| Cloudinary | Image storage |
| Bootstrap 5 | UI styling |
| Render | Cloud deployment |
| Gunicorn | Production web server |
| WhiteNoise | Static file serving |

## ⚙️ Local Setup

### Prerequisites
- Python 3.12+
- PostgreSQL
- Git

### Steps

```bash
# Clone the repository
git clone https://github.com/your-username/your-repo.git
cd your-repo

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file (see .env.example)
# Add your database and Cloudinary credentials

# Run migrations
python manage.py migrate
python manage.py setup_groups
python manage.py createsuperuser

# Start server
python manage.py runserver
```

## 👥 User Roles
| Role | Permissions |
|---|---|
| Standard User | View public albums, upload photos, edit own photos |
| Administrator | Full CRUD on all albums and photos, manage users |

## 📁 Project Structure
```
photoalbum/
├── core/          # Project settings and URLs
├── albums/        # Main app (models, views, forms)
├── templates/     # HTML templates
├── static/        # CSS and assets
├── requirements.txt
├── Procfile
├── render.yaml
└── README.md
```