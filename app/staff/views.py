from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from flask_rq import get_queue

from app import db

from app.decorators import staff_required, login_required
from app.models import EditableHTML, Role, RoomRequest

staff = Blueprint('staff', __name__)


@staff.route('/')
@login_required
@staff_required
def index():
    """Staff dashboard page."""
    roles = Role.query.all()
    room_requests = RoomRequest.query.all()
    return render_template('staff/index.html', roles=roles, room_requests=room_requests)


@staff_required
@staff.route('/room-request-form', methods=['GET'])
def manage():
    room_requests = RoomRequest.query.all()
    return render_template('room_request/manage.html', room_requests=room_requests)