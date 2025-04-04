# 📚 StudyBuddy

[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

A collaborative learning platform connecting students and teachers, facilitating knowledge sharing through notes, interactions, and personalized content.

## 📑 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Setup Instructions](#-setup-instructions)
- [Usage Tips](#-usage-tips)
- [Project Structure](#-project-structure)
- [Security Features](#-security-features)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 👥 User Management

- Custom user system with student and teacher roles
- Profile management with profile pictures
- Role-based access control (students and teachers)
- Grade level tracking for students
- Subject category specialization for teachers
- Follow system with request/accept mechanism

### 📝 Notes System

- Create and share educational notes
- File attachments support (PDF, images, etc.)
- Subject categorization (Mathematics, Science, History, etc.)
- Grade level classification (1st through 12th grade)
- Like/Dislike functionality for feedback
- Public/private note visibility options
- Rich text content support

### 🔔 Notification System

- Real-time notifications for user interactions
- Follow/unfollow system
- Notification types:
  - Follow requests and acceptances
  - Likes and dislikes
  - Comments
  - New note alerts

### 📁 Media Management

- Profile picture uploads
- Note file attachments
- Organized media storage system

### 🎨 User Interface

- Responsive design
- Interactive animations
- Modern and intuitive layout

## 🛠️ Technology Stack

### 🔧 Backend

- Django (Python web framework)
- Django REST Framework for API endpoints
- SQLite database (default)
- ASGI/WSGI support for deployment

### 🎯 Frontend

- Django Templates
- HTML5
- CSS3
- JavaScript (Vanilla)
- AJAX for async operations

### 🔐 Authentication

- Django Authentication System
- Custom user model

### 📂 File Handling

- Django File Storage
- Media file management

### 💾 File Storage

- Django's built-in file storage system
- Organized media directories for different content types

## 🚀 Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install django django-rest-framework Pillow
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## 💡 Usage Tips

### 👨‍🏫 For Teachers

- Select your subject specialization during registration
- Create and share notes relevant to your subject
- Monitor student interactions with your content

### 👨‍🎓 For Students

- Select your grade level during registration
- Follow teachers and peers for relevant content
- Interact with notes through likes and comments
- Manage your learning materials efficiently

## 📂 Project Structure

```
studybuddy/
├── notes/          # Note management application
├── notifications/  # Notification system
├── profile_users/  # User profile management
├── users/          # Custom user authentication
├── static/         # Static files (CSS, JS, images)
├── media/          # User-uploaded content
└── templates/      # HTML templates
```

## 🔒 Security Features

- Custom user authentication
- Role-based access control
- Secure file upload handling
- Protected user data and content

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
