# 🏋️ Rhose Gym Management System

A comprehensive web-based gym management system built with Django, featuring membership management, payment processing, staff management, attendance tracking, and an intelligent AI chatbot.

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Django](https://img.shields.io/badge/django-4.2+-green.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 📋 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [User Roles](#-user-roles)
- [Database Schema](#-database-schema)
- [Management Commands](#-management-commands)
- [API Endpoints](#-api-endpoints)
- [Project Structure](#-project-structure)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🎯 Core Features

#### Member Management
- ✅ Member registration and authentication
- ✅ Role-based access control (Admin, Staff, Member)
- ✅ Custom user model with demographic data
- ✅ Profile management with contact information
- ✅ Age calculation from birthdate
- ✅ Member search and filtering

#### Membership Plans
- ✅ Flexible membership plan creation (monthly, yearly, custom)
- ✅ Plan activation/deactivation
- ✅ Automatic membership expiration
- ✅ Days remaining calculation
- ✅ Renewal reminders
- ✅ Subscription management

#### Walk-in Management
- ✅ Flexible access passes (1-day, 3-day, weekly)
- ✅ Walk-in payment processing
- ✅ Customer information (optional)
- ✅ Payment confirmation workflow
- ✅ Transaction history

#### Payment System
- ✅ Multiple payment methods (Cash, GCash, Card)
- ✅ Payment confirmation before processing
- ✅ GCash QR code integration
- ✅ Payment history tracking
- ✅ Transaction reference numbers
- ✅ Revenue analytics

#### Staff Features
- ✅ Dedicated staff dashboard
- ✅ Process walk-in sales
- ✅ View payment history
- ✅ Member lookup
- ✅ Daily revenue tracking
- ✅ Staff account creation (admin only)

#### Admin Features
- ✅ Comprehensive admin dashboard
- ✅ Analytics and reporting
- ✅ Member and staff management
- ✅ Plan management interface
- ✅ Audit trail system
- ✅ Full system access

#### Attendance System
- ✅ Kiosk mode for self-service check-in/out
- ✅ Attendance tracking
- ✅ Duration calculation
- ✅ Attendance reports
- ✅ Currently checked-in members
- ✅ Daily attendance statistics

#### Intelligent Chatbot 🤖
- ✅ AI-powered assistant (ChatterBot)
- ✅ Natural language processing
- ✅ Database query capabilities
- ✅ Role-based information access
- ✅ Quick reply buttons
- ✅ Chat history persistence
- ✅ Real-time responses

#### Security & Audit
- ✅ Comprehensive audit logging
- ✅ IP address tracking
- ✅ User agent logging
- ✅ Action tracking (login, payment, etc.)
- ✅ Security event monitoring
- ✅ Failed login attempt tracking

#### User Interface
- ✅ Modern, responsive design
- ✅ Blue & gold color scheme
- ✅ Mobile-friendly layouts
- ✅ Font Awesome icons
- ✅ Smooth animations
- ✅ Toast notifications
- ✅ Print-friendly pages

---

## 📸 Screenshots

> Add screenshots of your application here

---

## 🛠️ Technology Stack

### Backend
- **Framework:** Django 4.2+
- **Language:** Python 3.8+
- **Database:** SQLite (Development) / PostgreSQL (Production)
- **Authentication:** Django Auth System
- **ORM:** Django ORM

### Frontend
- **HTML5 & CSS3**
- **JavaScript (Vanilla)**
- **Font Awesome Icons**
- **Google Fonts (Poppins)**
- **Responsive Design**

### AI & NLP
- **ChatterBot 1.0.8** - Conversational AI
- **NLTK** - Natural Language Processing
- **SQLAlchemy** - Chatbot storage

### Additional Libraries
- **Pillow** - Image processing
- **ReportLab** - PDF generation
- **OpenPyXL** - Excel export
- **QRCode** - QR code generation
- **python-dateutil** - Date utilities

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Virtual environment (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Natz789/Web-Based-Gym-System.git
cd Web-Based-Gym-System
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download NLTK Data (for Chatbot)

```bash
python -m nltk.downloader punkt
python -m nltk.downloader averaged_perceptron_tagger
python -m nltk.downloader stopwords
```

### Step 5: Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional, defaults to SQLite)
DATABASE_URL=postgresql://user:password@localhost/dbname

# Email Configuration (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Step 6: Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Create Admin User

```bash
python manage.py createadmin
```

Follow the prompts to create an admin account.

### Step 8: Load Sample Data (Optional)

```bash
python manage.py create_sample_data
```

### Step 9: Run Development Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

---

## ⚙️ Configuration

### Settings Overview

Key settings in `gym_project/settings.py`:

```python
# Custom User Model
AUTH_USER_MODEL = 'gym_app.User'

# Static Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Date/Time
USE_TZ = True
TIME_ZONE = 'Asia/Manila'
```

### Environment Variables

Create a `.env` file with:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `ALLOWED_HOSTS` - Comma-separated hosts
- `DATABASE_URL` - Database connection string

---

## 📖 Usage

### User Registration

1. Navigate to **http://127.0.0.1:8000/register/**
2. Fill in the registration form
3. Submit to create a member account
4. Login with your credentials

### Admin Dashboard

1. Login as admin
2. Access **http://127.0.0.1:8000/dashboard/**
3. View analytics:
   - Total members
   - Active memberships
   - Revenue statistics
   - Recent payments
   - Expiring memberships

### Subscribing to a Plan

1. Login as a member
2. Go to **Plans** menu
3. Browse available plans
4. Click **Subscribe** on desired plan
5. Select payment method
6. Confirm payment

### Processing Walk-in Sales (Staff/Admin)

1. Login as staff or admin
2. Go to **Walk-in** menu
3. Select pass type
4. Enter customer info (optional)
5. Choose payment method
6. Review and confirm

### Creating Staff Users (Admin)

1. Login as admin
2. Go to **Members** → **Members List**
3. Click **Create Staff** button
4. Fill in staff details
5. Submit to create account

### Using the Chatbot

1. Click the **chat icon** (bottom-right)
2. Type your question or use quick replies
3. Get instant responses
4. Ask about:
   - Membership plans
   - Payment methods
   - Your membership status
   - Walk-in passes
   - And more!

### Attendance Check-in (Kiosk Mode)

1. Visit **http://127.0.0.1:8000/kiosk/**
2. Enter username and password
3. Check in or check out
4. View session duration

---

## 👥 User Roles

### Admin
- **Full system access**
- Create/manage staff users
- View all reports and analytics
- Access Django admin panel
- Manage membership plans
- View audit trail
- Access all features

### Staff
- **Limited access**
- Process walk-in sales
- View member information
- View payment history
- Monitor daily revenue
- Cannot access reports or admin panel

### Member
- **Personal access only**
- View own dashboard
- Subscribe to plans
- View payment history
- Check membership status
- Renew membership

---

## 🗄️ Database Schema

### Core Models

#### User
- Custom user model extending AbstractBaseUser
- Fields: username, email, password, role, first_name, last_name, mobile_no, address, birthdate
- Methods: is_admin(), is_staff_or_admin(), calculate_age()

#### MembershipPlan
- Fields: name, duration_days, price, is_active, description
- Relationships: UserMembership (One-to-Many)

#### FlexibleAccess
- Fields: name, duration_days, price, is_active, description
- Relationships: WalkInPayment (One-to-Many)

#### UserMembership
- Fields: user, plan, start_date, end_date, status
- Methods: is_active(), days_remaining()
- Relationships: User (Many-to-One), MembershipPlan (Many-to-One)

#### Payment
- Fields: user, membership, amount, method, payment_date, reference_no
- Relationships: User (Many-to-One), UserMembership (Many-to-One)

#### WalkInPayment
- Fields: pass_type, customer_name, mobile_no, amount, method, payment_date
- Relationships: FlexibleAccess (Many-to-One)

#### AuditLog
- Fields: user, action, description, ip_address, timestamp, severity
- Methods: log(), get_user_activity(), get_security_events()

#### Attendance
- Fields: user, check_in, check_out, duration, notes
- Methods: calculate_duration()

---

## 🔧 Management Commands

### Custom Commands

#### Create Admin User
```bash
python manage.py createadmin
```
Creates a superuser with admin role.

Options:
- `--username` - Admin username
- `--email` - Admin email
- `--noinput` - Non-interactive mode

#### Sync User Roles
```bash
python manage.py sync_roles
```
Syncs superusers to admin role and staff users to staff role.

#### Expire Memberships
```bash
python manage.py expire_memberships
```
Automatically expires memberships past end_date.

#### Create Sample Data
```bash
python manage.py create_sample_data
```
Populates database with sample data for testing.

#### Cleanup Database
```bash
python manage.py cleanup_database
```
Removes old audit logs and expired sessions.

### Django Commands

```bash
# Migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver

# Django shell
python manage.py shell
```

---

## 🔌 API Endpoints

### Chatbot API

**POST** `/api/chatbot/`

Request:
```json
{
    "message": "What membership plans do you offer?"
}
```

Response:
```json
{
    "response": "Here are our available membership plans...",
    "timestamp": "2024-11-09T12:34:56.789Z"
}
```

---

## 📁 Project Structure

```
Web-Based-Gym-System/
├── gym_app/                        # Main application
│   ├── management/
│   │   └── commands/
│   │       ├── createadmin.py
│   │       ├── sync_roles.py
│   │       ├── expire_memberships.py
│   │       ├── create_sample_data.py
│   │       └── cleanup_database.py
│   ├── migrations/
│   ├── static/
│   │   └── gym_app/
│   │       ├── css/
│   │       │   ├── base/
│   │       │   ├── pages/
│   │       │   └── chatbot.css
│   │       ├── js/
│   │       │   └── chatbot.js
│   │       └── images/
│   ├── templates/
│   │   └── gym_app/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── dashboard_*.html
│   │       └── ...
│   ├── admin.py
│   ├── apps.py
│   ├── chatbot.py
│   ├── decoraters.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── gym_project/                    # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3                      # SQLite database
├── manage.py
├── requirements.txt
├── README.md
├── CHATBOT.md
├── STAFF.md
├── Phases1.md
└── ...
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test gym_app

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Manual Testing Checklist

- [ ] User registration and login
- [ ] Membership subscription
- [ ] Payment processing (all methods)
- [ ] Walk-in sales
- [ ] Staff user creation
- [ ] Attendance check-in/out
- [ ] Chatbot responses
- [ ] Report generation
- [ ] Audit trail logging
- [ ] Role-based access control

---

## 🚢 Deployment

### Production Setup

1. **Set Environment Variables**
```bash
export DEBUG=False
export SECRET_KEY=your-production-secret-key
export ALLOWED_HOSTS=yourdomain.com
```

2. **Configure Database**
```bash
# PostgreSQL
export DATABASE_URL=postgresql://user:password@localhost/gymdb
```

3. **Collect Static Files**
```bash
python manage.py collectstatic --noinput
```

4. **Apply Migrations**
```bash
python manage.py migrate
```

5. **Create Admin User**
```bash
python manage.py createadmin --noinput
```

### Deployment Platforms

- **Heroku** - Easy deployment with Procfile
- **DigitalOcean** - VPS deployment with Gunicorn + Nginx
- **AWS EC2** - Scalable cloud deployment
- **PythonAnywhere** - Simple Django hosting

### Using Gunicorn

```bash
pip install gunicorn
gunicorn gym_project.wsgi:application --bind 0.0.0.0:8000
```

### Using Nginx (Reverse Proxy)

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards

- Follow PEP 8 style guide
- Write descriptive commit messages
- Add docstrings to functions and classes
- Update documentation for new features
- Write tests for new functionality

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Authors

- **Natz789** - Initial work

---

## 🙏 Acknowledgments

- Django framework team
- ChatterBot contributors
- Font Awesome icons
- Google Fonts (Poppins)
- All open-source contributors

---

## 📞 Support

For support, email support@rhosegym.com or open an issue on GitHub.

---

## 🗺️ Roadmap

### Version 2.1 (Planned)
- [ ] Email notifications
- [ ] SMS integration
- [ ] PDF receipt generation
- [ ] Excel export functionality
- [ ] Enhanced analytics with Chart.js
- [ ] Profile photo uploads
- [ ] Bulk member import

### Version 3.0 (Future)
- [ ] Mobile app (React Native)
- [ ] Payment gateway integration
- [ ] Workout tracking
- [ ] Nutrition planning
- [ ] Personal trainer booking
- [ ] Class scheduling
- [ ] Equipment maintenance tracking

---

## 📊 Stats

- **Lines of Code:** 10,000+
- **Models:** 8
- **Views:** 20+
- **Templates:** 20+
- **Management Commands:** 5
- **Features:** 50+

---

## 🎉 Thank You!

Thank you for using Rhose Gym Management System! We hope it helps streamline your gym operations.

**Happy Gymming! 💪**

---

*Last Updated: November 2024*
*Version: 2.0.0*
