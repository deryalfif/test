from datetime import datetime, date
from flask import request, jsonify, send_file
from flask_login import login_required
from io import BytesIO
from . import api_bp
from database import db, Attendance, Student, Class, Journal, AcademicPeriod
from auth.utils import teacher_required


@api_bp.route('/reports/attendance/monthly', methods=['GET'])
@login_required
def monthly_attendance_report():
    """Generate monthly attendance report data"""
    class_id = request.args.get('class_id', type=int)
    month = request.args.get('month', date.today().month, type=int)
    year = request.args.get('year', date.today().year, type=int)

    if not class_id:
        return jsonify({'success': False, 'message': 'class_id required'}), 400

    students = Student.query.filter_by(class_id=class_id, is_active=True).all()
    report_data = []

    for student in students:
        records = Attendance.query.filter(
            Attendance.student_id == student.id,
            db.extract('month', Attendance.date) == month,
            db.extract('year', Attendance.date) == year
        ).all()

        summary = {
            'present': 0,
            'absent': 0,
            'sick': 0,
            'permitted': 0
        }

        daily_records = {}
        for record in records:
            summary[record.status] = summary.get(record.status, 0) + 1
            daily_records[record.date.day] = record.status

        total = sum(summary.values())
        report_data.append({
            'student_id': student.student_id,
            'student_name': student.full_name,
            'summary': summary,
            'total_days': total,
            'attendance_rate': round((summary['present'] / total * 100), 2) if total > 0 else 0,
            'daily': daily_records
        })

    return jsonify({
        'success': True,
        'report': {
            'class_id': class_id,
            'month': month,
            'year': year,
            'students': report_data
        }
    })


@api_bp.route('/reports/attendance/semester', methods=['GET'])
@login_required
def semester_attendance_report():
    """Generate semester attendance report data"""
    class_id = request.args.get('class_id', type=int)
    period_id = request.args.get('period_id', type=int)

    if not class_id:
        return jsonify({'success': False, 'message': 'class_id required'}), 400

    # Get academic period
    if period_id:
        period = AcademicPeriod.query.get(period_id)
    else:
        period = AcademicPeriod.query.filter_by(is_active=True).first()

    if not period:
        return jsonify({'success': False, 'message': 'No academic period found'}), 404

    students = Student.query.filter_by(class_id=class_id, is_active=True).all()
    report_data = []

    for student in students:
        records = Attendance.query.filter(
            Attendance.student_id == student.id,
            Attendance.date >= period.start_date,
            Attendance.date <= period.end_date
        ).all()

        summary = {
            'present': 0,
            'absent': 0,
            'sick': 0,
            'permitted': 0
        }

        for record in records:
            summary[record.status] = summary.get(record.status, 0) + 1

        total = sum(summary.values())
        report_data.append({
            'student_id': student.student_id,
            'student_name': student.full_name,
            'summary': summary,
            'total_days': total,
            'attendance_rate': round((summary['present'] / total * 100), 2) if total > 0 else 0
        })

    return jsonify({
        'success': True,
        'report': {
            'class_id': class_id,
            'period': {
                'id': period.id,
                'name': period.name,
                'start_date': period.start_date.isoformat(),
                'end_date': period.end_date.isoformat()
            },
            'students': report_data
        }
    })


@api_bp.route('/reports/journal/export', methods=['GET'])
@login_required
def export_journals():
    """Export journals data"""
    class_id = request.args.get('class_id', type=int)
    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)

    query = Journal.query

    if class_id:
        query = query.filter_by(class_id=class_id)
    if month and year:
        query = query.filter(
            db.extract('month', Journal.date) == month,
            db.extract('year', Journal.date) == year
        )

    journals = query.order_by(Journal.date).all()

    return jsonify({
        'success': True,
        'journals': [{
            'date': j.date.isoformat(),
            'subject': j.subject,
            'materials_covered': j.materials_covered,
            'activities': j.activities,
            'homework': j.homework,
            'notes': j.notes,
            'created_by': j.author.full_name if j.author else None
        } for j in journals]
    })


@api_bp.route('/reports/dashboard/summary', methods=['GET'])
@login_required
def dashboard_summary():
    """Get dashboard summary statistics"""
    today = date.today()

    # Today's attendance summary
    today_attendance = db.session.query(
        Attendance.status,
        db.func.count(Attendance.id)
    ).filter(
        Attendance.date == today
    ).group_by(Attendance.status).all()

    attendance_summary = {status: count for status, count in today_attendance}

    # Total counts
    total_students = Student.query.filter_by(is_active=True).count()
    total_classes = Class.query.count()

    # Recent journals
    recent_journals = Journal.query.order_by(Journal.date.desc()).limit(5).all()

    return jsonify({
        'success': True,
        'summary': {
            'today': today.isoformat(),
            'attendance_today': attendance_summary,
            'total_students': total_students,
            'total_classes': total_classes,
            'recent_journals': [{
                'id': j.id,
                'date': j.date.isoformat(),
                'subject': j.subject,
                'class_id': j.class_id
            } for j in recent_journals]
        }
    })
