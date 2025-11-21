from datetime import datetime, date
from flask import request, jsonify
from flask_login import login_required, current_user
from . import api_bp
from database import db, Journal, Class, Student
from auth.utils import teacher_required


@api_bp.route('/journal/class/<int:class_id>', methods=['GET'])
@login_required
def get_class_journals(class_id):
    """Get journals for a class"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    month = request.args.get('month')
    year = request.args.get('year')

    query = Journal.query.filter_by(class_id=class_id)

    if month and year:
        query = query.filter(
            db.extract('month', Journal.date) == month,
            db.extract('year', Journal.date) == year
        )

    journals = query.order_by(Journal.date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'success': True,
        'journals': [{
            'id': j.id,
            'date': j.date.isoformat(),
            'subject': j.subject,
            'materials_covered': j.materials_covered,
            'activities': j.activities,
            'homework': j.homework,
            'notes': j.notes,
            'created_by': j.author.full_name if j.author else None
        } for j in journals.items],
        'pagination': {
            'page': journals.page,
            'pages': journals.pages,
            'total': journals.total,
            'has_next': journals.has_next,
            'has_prev': journals.has_prev
        }
    })


@api_bp.route('/journal/<int:id>', methods=['GET'])
@login_required
def get_journal(id):
    """Get specific journal entry"""
    journal = Journal.query.get_or_404(id)

    return jsonify({
        'success': True,
        'journal': {
            'id': journal.id,
            'class_id': journal.class_id,
            'date': journal.date.isoformat(),
            'subject': journal.subject,
            'materials_covered': journal.materials_covered,
            'activities': journal.activities,
            'homework': journal.homework,
            'notes': journal.notes,
            'created_by': journal.author.full_name if journal.author else None,
            'created_at': journal.created_at.isoformat()
        }
    })


@api_bp.route('/journal', methods=['POST'])
@login_required
@teacher_required
def create_journal():
    """Create new journal entry"""
    data = request.get_json()

    journal = Journal(
        class_id=data.get('class_id'),
        date=datetime.strptime(data.get('date'), '%Y-%m-%d').date(),
        subject=data.get('subject'),
        materials_covered=data.get('materials_covered'),
        activities=data.get('activities'),
        homework=data.get('homework'),
        notes=data.get('notes'),
        created_by=current_user.id
    )

    db.session.add(journal)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Journal created successfully',
        'journal_id': journal.id
    }), 201


@api_bp.route('/journal/<int:id>', methods=['PUT'])
@login_required
@teacher_required
def update_journal(id):
    """Update journal entry"""
    journal = Journal.query.get_or_404(id)
    data = request.get_json()

    journal.subject = data.get('subject', journal.subject)
    journal.materials_covered = data.get('materials_covered', journal.materials_covered)
    journal.activities = data.get('activities', journal.activities)
    journal.homework = data.get('homework', journal.homework)
    journal.notes = data.get('notes', journal.notes)
    journal.updated_at = datetime.utcnow()

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Journal updated successfully'
    })


@api_bp.route('/journal/<int:id>', methods=['DELETE'])
@login_required
@teacher_required
def delete_journal(id):
    """Delete journal entry"""
    journal = Journal.query.get_or_404(id)

    db.session.delete(journal)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Journal deleted successfully'
    })


@api_bp.route('/journal/search', methods=['GET'])
@login_required
def search_journals():
    """Search journals by keyword"""
    keyword = request.args.get('q', '')
    class_id = request.args.get('class_id')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Journal.query

    if class_id:
        query = query.filter_by(class_id=class_id)

    if keyword:
        search = f'%{keyword}%'
        query = query.filter(
            db.or_(
                Journal.subject.ilike(search),
                Journal.materials_covered.ilike(search),
                Journal.activities.ilike(search)
            )
        )

    journals = query.order_by(Journal.date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'success': True,
        'journals': [{
            'id': j.id,
            'date': j.date.isoformat(),
            'subject': j.subject,
            'materials_covered': j.materials_covered[:100] + '...' if len(j.materials_covered) > 100 else j.materials_covered
        } for j in journals.items],
        'pagination': {
            'page': journals.page,
            'pages': journals.pages,
            'total': journals.total
        }
    })
