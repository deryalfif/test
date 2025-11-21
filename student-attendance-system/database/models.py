from datetime import datetime
from flask_login import UserMixin
from .database import db
import bcrypt


class AcademicPeriod(db.Model):
    """Academic period (semester/school year) model"""
    __tablename__ = 'academic_periods'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    year_start = db.Column(db.Integer, nullable=False)
    year_end = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    classes = db.relationship('Class', backref='academic_period', lazy='dynamic')
    schedules = db.relationship('Schedule', backref='academic_period', lazy='dynamic')

    def __repr__(self):
        return f'<AcademicPeriod {self.name}>'


class Class(db.Model):
    """Class model"""
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    grade_level = db.Column(db.Integer, nullable=False)
    academic_period_id = db.Column(db.Integer, db.ForeignKey('academic_periods.id'), nullable=False)
    homeroom_teacher = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    students = db.relationship('Student', backref='student_class', lazy='dynamic')
    journals = db.relationship('Journal', backref='journal_class', lazy='dynamic')
    schedules = db.relationship('Schedule', backref='schedule_class', lazy='dynamic')

    def __repr__(self):
        return f'<Class {self.name}>'


class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, teacher, parent
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    students = db.relationship('Student', backref='parent', lazy='dynamic')
    attendance_records = db.relationship('Attendance', backref='creator', lazy='dynamic')
    journals_created = db.relationship('Journal', backref='author', lazy='dynamic')
    calendar_syncs = db.relationship('GoogleCalendarSync', backref='user', lazy='dynamic')
    backups = db.relationship('BackupHistory', backref='creator', lazy='dynamic')

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    def check_password(self, password):
        """Verify password"""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

    def __repr__(self):
        return f'<User {self.username}>'


class Student(db.Model):
    """Student model"""
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    parent_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    address = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    attendance_records = db.relationship('Attendance', backref='student', lazy='dynamic')

    def __repr__(self):
        return f'<Student {self.full_name}>'


class Attendance(db.Model):
    """Attendance record model"""
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # present, absent, sick, permitted
    remarks = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('student_id', 'date', name='unique_student_date'),
    )

    def __repr__(self):
        return f'<Attendance {self.student_id} - {self.date}>'


class Journal(db.Model):
    """Daily learning journal model"""
    __tablename__ = 'journals'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    subject = db.Column(db.String(100))
    materials_covered = db.Column(db.Text, nullable=False)
    activities = db.Column(db.Text)
    homework = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Journal {self.class_id} - {self.date}>'


class Schedule(db.Model):
    """Class schedule model"""
    __tablename__ = 'schedules'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    teacher_name = db.Column(db.String(100))
    room = db.Column(db.String(50))
    academic_period_id = db.Column(db.Integer, db.ForeignKey('academic_periods.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Schedule {self.subject} - Day {self.day_of_week}>'


class GoogleCalendarSync(db.Model):
    """Google Calendar sync configuration"""
    __tablename__ = 'google_calendar_sync'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    calendar_id = db.Column(db.String(255))
    last_sync = db.Column(db.DateTime)
    sync_token = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<GoogleCalendarSync {self.user_id}>'


class BackupHistory(db.Model):
    """Backup history model"""
    __tablename__ = 'backup_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    backup_date = db.Column(db.DateTime, nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    google_drive_id = db.Column(db.String(255))
    file_size = db.Column(db.Integer)
    status = db.Column(db.String(20), nullable=False)  # success, failed, pending
    error_message = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<BackupHistory {self.file_name}>'
