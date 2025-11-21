# Student Attendance & Daily Journal System

## Project Overview

A web-based student attendance and daily journal system designed for small schools (20-30 students) with multi-class support, parent access portal, and Google Calendar integration.

## System Requirements

### Functional Requirements
- Multi-role authentication (Admin, Teacher, Parent)
- Student attendance tracking with multiple status options
- Daily learning journal for documenting materials covered
- Academic period management (Semester/School Year)
- Parent portal for viewing child's attendance
- Schedule management with Google Calendar sync
- Monthly/Semester attendance reports
- Google Drive backup capability
- Mobile-responsive design

### Non-Functional Requirements
- SQLite database (lightweight, serverless)
- Mobile-first responsive design
- Local deployment capability
- Offline-capable for basic operations
- Support for 20-30 students across multiple classes

## Technology Stack

### Backend
- **Framework**: Flask 3.0+
- **Database**: SQLite3
- **ORM**: SQLAlchemy 2.0+
- **Authentication**: Flask-Login
- **Session Management**: Flask-Session
- **API Integration**: Google Calendar API, Google Drive API
- **PDF Generation**: ReportLab
- **Excel Export**: openpyxl
- **Environment Management**: python-dotenv

### Frontend
- **HTML5** with semantic markup
- **CSS Framework**: Tailwind CSS 3.4+
- **JavaScript Framework**: Alpine.js 3.x (lightweight reactivity)
- **Calendar Component**: FullCalendar 6.x
- **Charts**: Chart.js 4.x
- **Icons**: Heroicons
- **PWA**: Service Worker for offline capability

## Database Schema

### 1. academic_periods
```sql
CREATE TABLE academic_periods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    year_start INTEGER NOT NULL,
    year_end INTEGER NOT NULL,
    semester INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. classes
```sql
CREATE TABLE classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    grade_level INTEGER NOT NULL,
    academic_period_id INTEGER NOT NULL,
    homeroom_teacher VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (academic_period_id) REFERENCES academic_periods(id)
);
```

### 3. users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'teacher', 'parent')),
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. students
```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id VARCHAR(20) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    class_id INTEGER NOT NULL,
    parent_user_id INTEGER,
    date_of_birth DATE,
    gender VARCHAR(10),
    address TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (class_id) REFERENCES classes(id),
    FOREIGN KEY (parent_user_id) REFERENCES users(id)
);
```

### 5. attendance
```sql
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    date DATE NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('present', 'absent', 'sick', 'permitted')),
    remarks TEXT,
    created_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    UNIQUE(student_id, date)
);
```

### 6. journals
```sql
CREATE TABLE journals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id INTEGER NOT NULL,
    date DATE NOT NULL,
    subject VARCHAR(100),
    materials_covered TEXT NOT NULL,
    activities TEXT,
    homework TEXT,
    notes TEXT,
    created_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (class_id) REFERENCES classes(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

### 7. schedules
```sql
CREATE TABLE schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL CHECK (day_of_week BETWEEN 0 AND 6),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    subject VARCHAR(100) NOT NULL,
    teacher_name VARCHAR(100),
    room VARCHAR(50),
    academic_period_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (class_id) REFERENCES classes(id),
    FOREIGN KEY (academic_period_id) REFERENCES academic_periods(id)
);
```

### 8. google_calendar_sync
```sql
CREATE TABLE google_calendar_sync (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    calendar_id VARCHAR(255),
    last_sync TIMESTAMP,
    sync_token TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 9. backup_history
```sql
CREATE TABLE backup_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    backup_date TIMESTAMP NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    google_drive_id VARCHAR(255),
    file_size INTEGER,
    status VARCHAR(20) NOT NULL CHECK (status IN ('success', 'failed', 'pending')),
    error_message TEXT,
    created_by INTEGER NOT NULL,
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

## Project Structure

```
student-attendance-system/
├── app.py                  # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── .gitignore            
├── README.md             
│
├── database/
│   ├── __init__.py
│   ├── models.py         # SQLAlchemy models
│   ├── database.py       # Database connection
│   └── migrations/       # Database migration scripts
│
├── auth/
│   ├── __init__.py
│   ├── routes.py         # Authentication routes
│   └── utils.py          # Auth helper functions
│
├── api/
│   ├── __init__.py
│   ├── attendance.py     # Attendance API endpoints
│   ├── journal.py        # Journal API endpoints
│   ├── schedule.py       # Schedule API endpoints
│   └── reports.py        # Report generation endpoints
│
├── services/
│   ├── __init__.py
│   ├── google_calendar.py  # Google Calendar integration
│   ├── google_drive.py     # Google Drive backup
│   ├── report_generator.py # PDF/Excel reports
│   └── backup_service.py   # Backup automation
│
├── static/
│   ├── css/
│   │   ├── main.css        # Custom styles
│   │   └── tailwind.css    # Tailwind CSS
│   ├── js/
│   │   ├── app.js          # Main JavaScript
│   │   ├── alpine.js       # Alpine.js
│   │   ├── chart.js        # Chart.js
│   │   └── calendar.js     # FullCalendar config
│   ├── images/
│   └── manifest.json       # PWA manifest
│
├── templates/
│   ├── base.html           # Base template
│   ├── auth/
│   │   ├── login.html
│   │   └── profile.html
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── users.html
│   │   ├── classes.html
│   │   └── settings.html
│   ├── teacher/
│   │   ├── dashboard.html
│   │   ├── attendance.html
│   │   ├── journal.html
│   │   └── schedule.html
│   ├── parent/
│   │   ├── dashboard.html
│   │   ├── attendance.html
│   │   └── journal.html
│   └── reports/
│       ├── monthly.html
│       └── semester.html
│
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_api.py
    └── test_services.py
```

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `GET /auth/profile` - Get user profile
- `PUT /auth/profile` - Update profile
- `POST /auth/change-password` - Change password

### Attendance
- `GET /api/attendance/class/{class_id}` - Get class attendance
- `GET /api/attendance/student/{student_id}` - Get student attendance
- `POST /api/attendance` - Submit attendance
- `PUT /api/attendance/{id}` - Update attendance
- `GET /api/attendance/report` - Generate attendance report

### Journal
- `GET /api/journal/class/{class_id}` - Get class journals
- `GET /api/journal/{id}` - Get specific journal
- `POST /api/journal` - Create journal entry
- `PUT /api/journal/{id}` - Update journal
- `DELETE /api/journal/{id}` - Delete journal

### Schedule
- `GET /api/schedule/class/{class_id}` - Get class schedule
- `POST /api/schedule` - Create schedule
- `PUT /api/schedule/{id}` - Update schedule
- `DELETE /api/schedule/{id}` - Delete schedule
- `POST /api/schedule/sync-google` - Sync with Google Calendar

### Reports
- `GET /api/reports/attendance/monthly` - Monthly attendance report
- `GET /api/reports/attendance/semester` - Semester attendance report
- `GET /api/reports/journal/export` - Export journals
- `POST /api/reports/generate-pdf` - Generate PDF report

### System
- `POST /api/system/backup` - Trigger backup
- `GET /api/system/backup-history` - Get backup history
- `POST /api/system/restore` - Restore from backup

## User Interface Design

### Mobile-First Approach
- Single column layout on mobile (<768px)
- Touch-friendly buttons (min 44x44px)
- Bottom navigation for mobile
- Swipe gestures for navigation
- Pull-to-refresh functionality

### Dashboard Components
1. **Admin Dashboard**
   - Today's attendance summary cards
   - Attendance chart by class
   - Recent journal entries
   - Quick actions panel
   - System notifications

2. **Teacher Dashboard**
   - Today's schedule
   - Quick attendance input
   - Recent journals
   - Class attendance overview

3. **Parent Dashboard**
   - Child's attendance percentage
   - Calendar view of attendance
   - Recent learning materials
   - Upcoming schedule

### Responsive Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

## Implementation Phases

### Phase 1: Core Foundation (Week 1-2)
- [ ] Setup Flask project structure
- [ ] Implement SQLAlchemy models
- [ ] Create database migrations
- [ ] Basic authentication system
- [ ] Admin user management

### Phase 2: Attendance System (Week 2-3)
- [ ] Attendance input interface
- [ ] Attendance viewing for all roles
- [ ] Basic attendance reports
- [ ] Attendance statistics

### Phase 3: Journal System (Week 3-4)
- [ ] Journal CRUD operations
- [ ] Journal viewing for parents
- [ ] Journal search functionality

### Phase 4: Schedule Management (Week 4-5)
- [ ] Schedule CRUD operations
- [ ] Calendar view implementation
- [ ] Google Calendar integration (read/write)
- [ ] Schedule conflict detection

### Phase 5: Reporting & Export (Week 5-6)
- [ ] Monthly attendance reports
- [ ] Semester reports
- [ ] PDF generation
- [ ] Excel export functionality

### Phase 6: Advanced Features (Week 6-7)
- [ ] Google Drive backup
- [ ] PWA implementation
- [ ] Offline capability
- [ ] Performance optimization

### Phase 7: Testing & Deployment (Week 7-8)
- [ ] Unit testing
- [ ] Integration testing
- [ ] User acceptance testing
- [ ] Local deployment setup
- [ ] Documentation completion

## Security Considerations

1. **Authentication**
   - Bcrypt for password hashing
   - Session timeout after 30 minutes of inactivity
   - CSRF protection on all forms

2. **Authorization**
   - Role-based access control (RBAC)
   - Parents can only view their children's data
   - Teachers can only modify their class data

3. **Data Protection**
   - SQLite database encryption
   - HTTPS enforcement in production
   - Regular automated backups

4. **Input Validation**
   - Server-side validation for all inputs
   - SQL injection prevention via SQLAlchemy
   - XSS protection in templates

## Performance Optimization

1. **Database**
   - Proper indexing on frequently queried columns
   - Query optimization with eager loading
   - Connection pooling

2. **Frontend**
   - Lazy loading for images
   - Minified CSS/JS in production
   - CDN for static assets

3. **Caching**
   - Redis for session storage (optional)
   - Browser caching for static files
   - API response caching

## Backup Strategy

1. **Automated Daily Backups**
   - SQLite database file
   - Uploaded files (if any)
   - Configuration files

2. **Google Drive Integration**
   - Automated upload to Google Drive
   - Retention policy (keep 30 days)
   - Versioning for database backups

3. **Recovery Procedure**
   - Download from Google Drive
   - Verify backup integrity
   - Restore to local system

## Configuration File (.env)

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///attendance.db
DATABASE_BACKUP_PATH=./backups

# Google API
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_CALENDAR_ID=primary
GOOGLE_DRIVE_FOLDER_ID=your-backup-folder-id

# Application Settings
ITEMS_PER_PAGE=20
SESSION_LIFETIME_MINUTES=30
MAX_UPLOAD_SIZE_MB=10

# Time Zone
TIMEZONE=Asia/Jakarta
```

## Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use ESLint for JavaScript
- Consistent naming conventions

### Git Workflow
- Main branch for production
- Develop branch for development
- Feature branches for new features
- Commit messages in present tense

### Testing Requirements
- Unit test coverage > 80%
- Integration tests for API endpoints
- UI tests for critical paths

## Deployment Instructions

### Local Deployment

1. **Prerequisites**
   ```bash
   Python 3.10+
   Node.js 18+
   SQLite3
   ```

2. **Installation**
   ```bash
   # Clone repository
   git clone <repository-url>
   cd student-attendance-system

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Install frontend dependencies
   npm install

   # Build Tailwind CSS
   npm run build-css
   ```

3. **Database Setup**
   ```bash
   # Create database
   python manage.py db init
   python manage.py db migrate
   python manage.py db upgrade

   # Create admin user
   python manage.py create-admin
   ```

4. **Run Application**
   ```bash
   # Development mode
   flask run --host=0.0.0.0 --port=5000

   # Production mode
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

5. **Access Application**
   - Open browser: http://localhost:5000
   - Login with admin credentials

## Troubleshooting Guide

### Common Issues

1. **Database Locked Error**
   - Solution: Implement proper connection pooling
   - Use WAL mode for SQLite

2. **Google API Rate Limits**
   - Solution: Implement exponential backoff
   - Cache API responses

3. **Mobile Layout Issues**
   - Solution: Test on real devices
   - Use browser developer tools

## Future Enhancements

1. **Version 2.0**
   - Student self-service portal
   - WhatsApp notification integration
   - Biometric attendance option
   - Multi-language support

2. **Version 3.0**
   - AI-powered attendance predictions
   - Integration with school management system
   - Advanced analytics dashboard
   - Multi-school support

## License

This project is proprietary software. All rights reserved.

## Support & Contact

For technical support or questions, please contact the development team.

---

*Last Updated: November 2024*
*Version: 1.0.0*