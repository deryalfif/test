from datetime import datetime, date
from flask import request, jsonify
from flask_login import login_required, current_user
from . import api_bp
from database import db, Attendance, Student, Class
from auth.utils import teacher_required


@api_bp.route('/attendance/class/<int:class_id>', methods=['GET'])
@login_required
def get_class_attendance(class_id):
    """Get attendance for a class"""
    date_str = request.args.get('date', date.today().isoformat())
    target_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    students = Student.query.filter_by(class_id=class_id, is_active=True).all()
    attendance_data = []

    for student in students:
        attendance = Attendance.query.filter_by(
            student_id=student.id,
            date=target_date
        ).first()

        attendance_data.append({
            'student_id': student.id,
            'student_name': student.full_name,
            'student_number': student.student_id,
            'status': attendance.status if attendance else None,
            'remarks': attendance.remarks if attendance else None
        })

    return jsonify({
        'success': True,
        'date': date_str,
        'class_id': class_id,
        'attendance': attendance_data
    })


@api_bp.route('/attendance/student/<int:student_id>', methods=['GET'])
@login_required
def get_student_attendance(student_id):
    """Get attendance history for a student"""
    student = Student.query.get_or_404(student_id)

    # Parents can only view their children's attendance
    if current_user.role == 'parent' and student.parent_user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Access denied'}), 403

    month = request.args.get('month', date.today().month)
    year = request.args.get('year', date.today().year)

    attendance_records = Attendance.query.filter(
        Attendance.student_id == student_id,
        db.extract('month', Attendance.date) == month,
        db.extract('year', Attendance.date) == year
    ).order_by(Attendance.date).all()

    return jsonify({
        'success': True,
        'student': {
            'id': student.id,
            'name': student.full_name,
            'student_id': student.student_id
        },
        'attendance': [{
            'date': record.date.isoformat(),
            'status': record.status,
            'remarks': record.remarks
        } for record in attendance_records]
    })


@api_bp.route('/attendance', methods=['POST'])
@login_required
@teacher_required
def submit_attendance():
    """Submit attendance for multiple students"""
    data = request.get_json()
    target_date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
    records = data.get('records', [])

    for record in records:
        student_id = record.get('student_id')
        status = record.get('status')
        remarks = record.get('remarks', '')

        # Check if attendance already exists
        existing = Attendance.query.filter_by(
            student_id=student_id,
            date=target_date
        ).first()

        if existing:
            existing.status = status
            existing.remarks = remarks
            existing.updated_at = datetime.utcnow()
        else:
            attendance = Attendance(
                student_id=student_id,
                date=target_date,
                status=status,
                remarks=remarks,
                created_by=current_user.id
            )
            db.session.add(attendance)

    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Attendance saved for {len(records)} students'
    })


@api_bp.route('/attendance/<int:id>', methods=['PUT'])
@login_required
@teacher_required
def update_attendance(id):
    """Update single attendance record"""
    attendance = Attendance.query.get_or_404(id)
    data = request.get_json()

    attendance.status = data.get('status', attendance.status)
    attendance.remarks = data.get('remarks', attendance.remarks)
    attendance.updated_at = datetime.utcnow()

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Attendance updated'
    })


@api_bp.route('/attendance/stats/class/<int:class_id>', methods=['GET'])
@login_required
def get_class_attendance_stats(class_id):
    """Get attendance statistics for a class"""
    month = request.args.get('month', date.today().month)
    year = request.args.get('year', date.today().year)

    students = Student.query.filter_by(class_id=class_id, is_active=True).all()
    stats = []

    for student in students:
        records = Attendance.query.filter(
            Attendance.student_id == student.id,
            db.extract('month', Attendance.date) == month,
            db.extract('year', Attendance.date) == year
        ).all()

        present = sum(1 for r in records if r.status == 'present')
        absent = sum(1 for r in records if r.status == 'absent')
        sick = sum(1 for r in records if r.status == 'sick')
        permitted = sum(1 for r in records if r.status == 'permitted')
        total = len(records)

        stats.append({
            'student_id': student.id,
            'student_name': student.full_name,
            'present': present,
            'absent': absent,
            'sick': sick,
            'permitted': permitted,
            'total': total,
            'percentage': round((present / total * 100), 2) if total > 0 else 0
        })

    return jsonify({
        'success': True,
        'class_id': class_id,
        'month': month,
        'year': year,
        'statistics': stats
    })
