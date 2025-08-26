# TikTube - Online Video Sharing Website by Django

A Django-powered video sharing platform with user authentication, video upload, and interactive features.

## Features

- Video upload and streaming
- User authentication (login/signup)
- Like/Dislike functionality with toggle
- Comment system
- Responsive design with Bootstrap
- Video search functionality
- Pagination

## Tech Stack

- **Backend**: Django 4.2
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: SQLite (development)
- **Icons**: Font Awesome
- **Video Player**: Custom HTML5 video player

## Installation & Setup

### Prerequisites
- Python 3.10+

### 1. Clone the Repository
```bash
git clone git@github.com:rakibulislam8226/tiktube.git
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 6. Go to src directory
```bash
cd src
```

### 6. Migrate Database
```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to view the application.

## Usage

### For Users
1. **Sign Up**: Create a new account
2. **Login**: Access your account
3. **Upload Videos**: Share your content
4. **Browse Videos**: Discover content from other users
5. **Interact**: Like, dislike, and comment on videos
