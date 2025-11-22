# Troubleshooting Guide

## Error 500 - Internal Server Error

Jika Anda mengalami error 500, coba langkah-langkah berikut:

### 1. Periksa Dependencies

```bash
# Pastikan virtual environment aktif
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows

# Install ulang dependencies
pip install -r requirements.txt
```

### 2. Inisialisasi Database

Error 500 sering terjadi karena database belum diinisialisasi:

```bash
# Hapus database lama (jika ada)
rm instance/attendance.db

# Inisialisasi ulang
flask init-db
flask create-admin
```

### 3. Periksa File .env

Pastikan file `.env` ada dan berisi konfigurasi yang benar:

```bash
cp .env.example .env
```

Edit `.env` dan pastikan `SECRET_KEY` terisi.

### 4. Buat Direktori yang Dibutuhkan

```bash
mkdir -p flask_session
mkdir -p backups
mkdir -p instance
```

### 5. Debug Mode

Jalankan aplikasi dalam debug mode untuk melihat error detail:

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
flask run
```

Atau langsung dengan Python:

```bash
python app.py
```

### 6. Periksa Log Error

Cek terminal untuk melihat traceback error yang lebih detail.

## Error Umum Lainnya

### ModuleNotFoundError

**Masalah:** `ModuleNotFoundError: No module named 'flask'`

**Solusi:**
```bash
# Pastikan virtual environment aktif
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Database Locked

**Masalah:** `sqlite3.OperationalError: database is locked`

**Solusi:**
```bash
# Tutup semua koneksi database
# Restart aplikasi
```

### Template Not Found

**Masalah:** `jinja2.exceptions.TemplateNotFound`

**Solusi:**
```bash
# Pastikan folder templates ada
ls -la templates/

# Periksa struktur folder
```

### Port Already in Use

**Masalah:** Port 5000 sudah digunakan

**Solusi:**
```bash
# Gunakan port lain
flask run --port 5001

# Atau hentikan proses di port 5000
lsof -ti:5000 | xargs kill -9  # Linux/Mac
```

## Quick Fix Script

Gunakan script setup untuk instalasi otomatis:

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

## Periksa Instalasi

```bash
# Test import
python -c "from app import create_app; app = create_app(); print('OK')"

# Periksa database
ls -la instance/

# Periksa dependencies
pip list | grep -i flask
```

## Masih Error?

1. Pastikan Python versi 3.10 atau lebih tinggi
2. Hapus `__pycache__` dan `*.pyc`:
   ```bash
   find . -type d -name __pycache__ -exec rm -rf {} +
   find . -type f -name "*.pyc" -delete
   ```
3. Reinstall virtual environment:
   ```bash
   rm -rf venv
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Kontak Support

Jika masalah masih berlanjut, sertakan informasi berikut:
- Python version: `python --version`
- OS: Windows/Linux/Mac
- Error message lengkap dari terminal
- Langkah yang sudah dicoba
