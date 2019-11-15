from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from flask_rq import get_queue
from app import db

import os
import datetime
import urllib

import sqlalchemy
from sqlalchemy import create_engine, not_, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from .forms import RoomRequestForm, ActivityForm, TransferForm
from .helpers import get_room_request_from_form get_form_from_room_request
from ..decorators import admin_required
from ..email import send_email
from ..models import Activity, EditableHTML, RoomRequest, User, Role

room_request = Blueprint('room_request', __name__)


@login_required
@room_request.route('/')
def dashboard():
    """View all room requests."""
    room_requests = RoomRequest.query.all()
    return render_template('room_request/dashboard.html', room_requests=room_requests)


@login_required
@room_request.route('/<int:id>/manage')
@room_request.route('/<int:id>/info')
def manage(id):
    """Manage room request."""
    room_request = RoomRequest.query.get(id)
    if room_request is None:
        return abort(404)
    return render_template('room_request/manage.html', room_request=room_request)


@login_required
@room_request.route('/<int:id>/patient')
def patient_info(id):
    """View patient info of given room request."""
    room_request = RoomRequest.query.get(id)
    if room_request is None:
        return abort(404)
    return render_template('room_request/manage.html', room_request=room_request)


@login_required
@room_request.route('/<int:id>/room-occupancy')
def room_occupancy_info(id):
    """View room occupancy needs for given room request."""
    room_request = RoomRequest.query.get(id)
    if room_request is None:
        return abort(404)
    return render_template('room_request/manage.html', room_request=room_request)


@login_required
@room_request.route('/<int:id>/guests')
def guest_info(id):
    """View table of guests for given room request."""
    room_request = RoomRequest.query.get(id)
    if room_request is None:
        return abort(404)
    return render_template('room_request/manage.html', room_request=room_request)


@login_required
@room_request.route('/<int:id>/edit')
def edit(id):
    """Edit room request info."""
    room_request = RoomRequest.query.get(id)
    if room_request is None:
        return abort(404)
    
    form = get_form_from_room_request(room_request)
    if form.validate_on_submit():
        room_request = get_room_request_from_form(form)
        try:
            db.session.add(room_request)
            db.session.commit()
            flash('Successfully saved changes.', 'form-success')
        except IntegrityError:
            db.session.rollback()
            flash('Unable to save changes. Please try again.', 'form-error')
    return render_template('room_request/manage.html', room_request=room_request, form=form)


@login_required
@room_request.route('<int:id>/delete')
def delete(id):
    """Request deletion of a room request, but does not actually perform the action until user confirmation."""
    room_request = RoomRequest.query.get(id)
    if room_request is None:
        return abort(404)
    return render_template('room_request/manage.html', room_request=room_request)


@login_required
@room_request.route('<int:id>/_delete')
def _delete(id):
    """Delete a room request."""
    room_request = RoomRequest.query.get(id)
    if room_request:
        db.session.delete(room_request)
        db.session.commit()
        flash(f'Successfully deleted room request for {room_request.first_name} {room_request.last_name}.', 'success')
    return redirect(url_for('room_request.dashboard'))


@login_required
@room_request.route('/new', methods=['GET', 'POST'])
def new():
    """Room Request page."""
    editable_html_obj = EditableHTML.get_editable_html('room_request')
    form = RoomRequestForm()
    if form.validate_on_submit():
        room_request = get_room_request_from_form(form)
        try:
            db.session.add(room_request)
            db.session.commit()
            get_queue().enqueue(
                send_email,
                recipient=room_request.email,
                subject='PRMH Room Request Submitted',
                template='room_request/confirmation_email',
                roomreq=room_request)
            flash('Successfully saved changes.', 'form-success')
        except IntegrityError:
            db.session.rollback()
            flash('Unable to save changes. Please try again.', 'form-error')
        flash('Successfully submitted form', 'form-success')
    return render_template('room_request/new.html', form=form, editable_html_obj=editable_html_obj)
    

@login_required
@room_request.route('/<int:id>', methods=['GET', 'POST'])
def view(id):    
    room_request = RoomRequest.query.get(id)
    if room_request is None:
        return abort(404)

    comments = Activity.query.filter_by(room_request_id=id)
    activity_form = ActivityForm()
    transfer_form = TransferForm()

    if activity_form.validate_on_submit():
        activity = Activity(
            text=activity_form.body.data,
            user_id=current_user.id,
            room_request_id=room_request.id)
        try:
            db.session.add(activity)
            db.session.commit()
            flash("Your comment has been added to the post", 'form-post')
        except:
            db.session.rollback()
        activity_form.body.data = ''


    if transfer_form.validate_on_submit():
        flash("Succesfully transferred!")

    return render_template('room_request/id.html',
        id=id,
        room_request=room_request,
        activity_form=activity_form,
        transfer_form=transfer_form,
        comments=comments)


@login_required
@room_request.route('/<int:id>/transfer', methods=['GET', 'POST'])
def transfer(id):
    room_request = RoomRequest.query.get(id)
    if room_request is None:
        return abort(404)

    transferred = False
    param_string = "DRIVER={};SERVER={};DATABASE={};UID={};PWD={}".format(
            os.getenv('SQL_SERVER') or "{SQL Server}",
            os.getenv('AZURE_SERVER'),
            os.getenv('AZURE_DATABASE'),
            os.getenv('AZURE_USERNAME'),
            os.getenv('AZURE_PASS'))
    params = urllib.parse.quote_plus(param_string)    
    engine = sqlalchemy.engine.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
    session = sessionmaker(bind=engine)()

    try:
        session.add(session.merge(room_request))
        session.commit()
        transferred = True
        flash('Room request succesfully transferred!', 'form-transfer')
        return redirect(url_for('room_request.view', id=id))
    except Exception as e:
        session.rollback()
        return render_template('room_request/transfer.html', id=id, transferred=transferred, error=e)


@login_required
@room_request.route('/<int:id>/duplicates', methods=['GET', 'POST'])
def duplicate_room_requests(id):
    room_request = RoomRequest.query.get(id)
    if room_request is None:
        return abort(404)
    # Duplicate room request must have:
    # (1) The same patient name
    # (2) A matching phone number or email for the requester
    duplicate_room_requests = RoomRequest.query \
        .filter_by(patient_first_name=room_request.patient_first_name, patient_last_name=room_request.patient_last_name) \
        .filter(or_(
            RoomRequest.primary_phone == room_request.primary_phone,
            RoomRequest.email == room_request.email,
        )) \
        .filter(RoomRequest.id != room_request.id) \
        .all();
    return render_template('room_request/duplicates.html', duplicate_room_requests=duplicate_room_requests)

