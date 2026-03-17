# PIMS - Placements and Internships Management System

A comprehensive Django-based web application designed to streamline the entire placements and internships lifecycle, from job posting to placement record management. PIMS facilitates seamless collaboration between students, recruiters, and placement officers.

## 🌟 Key Features

### For Students
- **User Profile Management** - Complete personal and academic profile setup
- **Job Discovery** - Browse and search available opportunities
- **Application Submission** - Apply for job opportunities with resume uploads
- **Application Tracking** - Monitor application status and feedback
- **Interview Management** - View scheduled interviews and interview results
- **Placement Records** - Access placement confirmation and placement details

### For Recruiters
- **Company Management** - Register and manage company information
- **Job Posting** - Create and publish job opportunities with detailed requirements
- **Skill Matching** - Define required skills with proficiency levels
- **Application Review** - Screen and review student applications
- **Interview Scheduling** - Schedule and conduct interviews
- **Placement Confirmation** - Confirm selected candidates

### For Placement Officers
- **System Administration** - Manage users and approvals
- **Company Approval** - Verify and approve recruiter companies
- **Recruiter Verification** - Approve/reject recruiter registrations
- **Dashboard Analytics** - View placement statistics and metrics
- **Notification Management** - Monitor system notifications

## 🛠️ Tech Stack

- **Backend Framework:** Django 6.0.1
- **Database:** SQLite (Development) / PostgreSQL (Production)
- **Frontend:** HTML5, CSS3, JavaScript
- **Server:** Gunicorn
- **Static Files:** WhiteNoise
- **Additional Libraries:**
  - Pillow (Image processing)
  - Django Simple Captcha (CAPTCHA security)
  - psycopg2-binary (PostgreSQL adapter)
  - dj-database-url (Database configuration)

## 📋 Project Structure

```
pims/
├── accounts/              # User authentication & management
├── applications/          # Job application handling
├── companies/             # Company management
├── dashboard/             # Dashboard views for different roles
├── decisions/             # Decision tracking
├── interviews/            # Interview scheduling & results
├── opportunities/         # Job opportunities management
├── records/               # Placement records
├── screening/             # Application screening process
├── students/              # Student profile management
├── media/                 # User uploads (resumes, profile images)
├── static/                # Static assets (CSS, JS, images)
├── templates/             # HTML templates
├── pims/                  # Project settings
├── manage.py              # Django management script
└── db.sqlite3            # SQLite database (development)
```

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/pims.git
   cd pims
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create Superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   - Open your browser and navigate to `http://localhost:8000`
   - Admin panel: `http://localhost:8000/admin`

## 🔐 User Roles

### Student
- Browse job opportunities
- Submit applications with resume
- Track application status
- View interview schedules
- Check placement records

### Recruiter
- Post job opportunities
- Define required skills
- Review student applications
- Schedule interviews
- Confirm placements
- *Requires account approval by Officer*

### Officer
- Administrative access
- Approve/reject recruiter registrations
- Verify company information
- View system-wide analytics
- Manage notifications

## 📖 Core Workflow

### 1. Job Publication
- Recruiter posts opportunity
- Defines required skills and qualifications
- Sets application deadline
- Opportunity becomes visible to students

### 2. Student Application
- Student discovers opportunity
- Submits application with resume
- Enters required information

### 3. Screening & Selection
- Recruiter reviews applications
- Conducts interviews
- Selects candidates

### 4. Placement Confirmation
- Selected candidates confirmed
- Placement records created
- Confirmation sent to students

## ⚙️ Configuration

### Environment Variables (Production)
Create a `.env` file in the project root:
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgres://user:password@localhost/pims
```

### Database Configuration
The system supports both SQLite (development) and PostgreSQL (production):
```python
# Development (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Production (PostgreSQL)
# Use dj-database-url to configure from DATABASE_URL
```

## 📱 Key Models

- **CustomUser** - Extended user model with roles (Student, Recruiter, Officer)
- **Company** - Company information
- **Opportunity** - Job postings with requirements
- **Application** - Student applications for opportunities
- **Interview** - Interview scheduling and results
- **Decision** - Final selection decisions
- **PlacementRecord** - Confirmed placements
- **StudentProfile** - Extended student information

## 🧪 Testing

Run tests for all apps:
```bash
python manage.py test
```

Run tests for a specific app:
```bash
python manage.py test accounts
```

## 📝 Available Commands

```bash
# Run development server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Shell access
python manage.py shell

# Run tests
python manage.py test
```


### Using WhiteNoise for Static Files
Static files are configured to be served via WhiteNoise for production efficiency.

Collect static files before deployment:
```bash
python manage.py collectstatic --noinput
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.


## 🆘 Troubleshooting

### Common Issues

**Issue: Database migrations fail**
```bash
# Reset migrations (development only)
python manage.py migrate accounts zero
python manage.py migrate
```

**Issue: Static files not loading**
```bash
python manage.py collectstatic --clear --noinput
```

**Issue: Permission denied on uploads**
- Ensure media folder has proper write permissions
- Check `MEDIA_ROOT` and `MEDIA_URL` settings

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Best Practices](https://docs.djangoproject.com/en/6.0/topics/db/models/)
- [Project Workflow Guide](./WORKFLOW_GUIDE.md)

## 📧 Support

For support, please open an issue on GitHub or contact the development team.

---

**Last Updated:** March 2026
