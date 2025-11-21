# Student Attendance System

Sistem absensi siswa dan jurnal harian berbasis web untuk sekolah kecil (20-30 siswa).

## Fitur

- Multi-role authentication (Admin, Teacher, Parent)
- Tracking absensi siswa (Hadir, Sakit, Izin, Absen)
- Jurnal pembelajaran harian
- Manajemen jadwal kelas
- Laporan kehadiran bulanan/semester
- Mobile-responsive design

## Tech Stack

- **Backend:** Flask 3.0+, SQLAlchemy, SQLite
- **Frontend:** Tailwind CSS, Alpine.js
- **Authentication:** Flask-Login

## Instalasi

```bash
# Clone repository
git clone <repository-url>
cd student-attendance-system

# Buat virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Inisialisasi database
flask init-db
flask create-admin

# Jalankan aplikasi
flask run
```

## Akun Default

- **Username:** admin
- **Password:** admin123

## Struktur Project

```
student-attendance-system/
├── app.py              # Main Flask application
├── config.py           # Configuration
├── database/           # Database models
├── auth/               # Authentication
├── api/                # REST API endpoints
├── templates/          # HTML templates
├── static/             # CSS, JS, images
└── tests/              # Unit tests
```

## API Endpoints

- `POST /auth/login` - Login
- `GET /api/attendance/class/{id}` - Get attendance
- `POST /api/attendance` - Submit attendance
- `GET /api/journal/class/{id}` - Get journals
- `POST /api/journal` - Create journal

## License

Proprietary - All rights reserved.
