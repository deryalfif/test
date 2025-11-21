from datetime import datetime
from flask import request, jsonify
from flask_login import login_required, current_user
from . import api_bp
from database import db, Schedule, Class, AcademicPeriod
from auth.utils import teacher_required, admin_required


DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


@api_bp.route('/schedule/class/<int:class_id>', methods=['GET'])
@login_required
def get_class_schedule(class_id):
    """Get schedule for a class"""
    schedules = Schedule.query.filter_by(class_id=class_id).order_by(
        Schedule.day_of_week, Schedule.start_time
    ).all()

    # Group by day
    schedule_by_day = {i: [] for i in range(7)}
    for s in schedules:
        schedule_by_day[s.day_of_week].append({
            'id': s.id,
            'subject': s.subject,
            'start_time': s.start_time.strftime('%H:%M'),
            'end_time': s.end_time.strftime('%H:%M'),
            'teacher_name': s.teacher_name,
            'room': s.room
        })

    return jsonify({
        'success': True,
        'class_id': class_id,
        'schedule': {
            DAYS_OF_WEEK[day]: items
            for day, items in schedule_by_day.items()
            if items  # Only include days with schedules
        }
    })


@api_bp.route('/schedule', methods=['POST'])
@login_required
@admin_required
def create_schedule():
    """Create schedule entry"""
    data = request.get_json()

    # Get active academic period
    active_period = AcademicPeriod.query.filter_by(is_active=True).first()
    if not active_period:
        return jsonify({
            'success': False,
            'message': 'No active academic period'
        }), 400

    schedule = Schedule(
        class_id=data.get('class_id'),
        day_of_week=data.get('day_of_week'),
        start_time=datetime.strptime(data.get('start_time'), '%H:%M').time(),
        end_time=datetime.strptime(data.get('end_time'), '%H:%M').time(),
        subject=data.get('subject'),
        teacher_name=data.get('teacher_name'),
        room=data.get('room'),
        academic_period_id=active_period.id
    )

    # Check for conflicts
    conflicts = Schedule.query.filter(
        Schedule.class_id == schedule.class_id,
        Schedule.day_of_week == schedule.day_of_week,
        Schedule.academic_period_id == active_period.id,
        db.or_(
            db.and_(
                Schedule.start_time <= schedule.start_time,
                Schedule.end_time > schedule.start_time
            ),
            db.and_(
                Schedule.start_time < schedule.end_time,
                Schedule.end_time >= schedule.end_time
            )
        )
    ).first()

    if conflicts:
        return jsonify({
            'success': False,
            'message': 'Schedule conflict detected'
        }), 400

    db.session.add(schedule)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Schedule created successfully',
        'schedule_id': schedule.id
    }), 201


@api_bp.route('/schedule/<int:id>', methods=['PUT'])
@login_required
@admin_required
def update_schedule(id):
    """Update schedule entry"""
    schedule = Schedule.query.get_or_404(id)
    data = request.get_json()

    if 'start_time' in data:
        schedule.start_time = datetime.strptime(data['start_time'], '%H:%M').time()
    if 'end_time' in data:
        schedule.end_time = datetime.strptime(data['end_time'], '%H:%M').time()

    schedule.subject = data.get('subject', schedule.subject)
    schedule.teacher_name = data.get('teacher_name', schedule.teacher_name)
    schedule.room = data.get('room', schedule.room)
    schedule.day_of_week = data.get('day_of_week', schedule.day_of_week)

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Schedule updated successfully'
    })


@api_bp.route('/schedule/<int:id>', methods=['DELETE'])
@login_required
@admin_required
def delete_schedule(id):
    """Delete schedule entry"""
    schedule = Schedule.query.get_or_404(id)

    db.session.delete(schedule)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Schedule deleted successfully'
    })


@api_bp.route('/schedule/today', methods=['GET'])
@login_required
def get_today_schedule():
    """Get today's schedule"""
    today = datetime.now().weekday()  # 0=Monday
    class_id = request.args.get('class_id', type=int)

    query = Schedule.query.filter_by(day_of_week=today)
    if class_id:
        query = query.filter_by(class_id=class_id)

    schedules = query.order_by(Schedule.start_time).all()

    return jsonify({
        'success': True,
        'day': DAYS_OF_WEEK[today],
        'schedules': [{
            'id': s.id,
            'class_id': s.class_id,
            'subject': s.subject,
            'start_time': s.start_time.strftime('%H:%M'),
            'end_time': s.end_time.strftime('%H:%M'),
            'teacher_name': s.teacher_name,
            'room': s.room
        } for s in schedules]
    })
