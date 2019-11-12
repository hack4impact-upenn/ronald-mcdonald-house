from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required

import os
import datetime
import urllib

import sqlalchemy
from sqlalchemy import create_engine, not_, or_
from sqlalchemy.orm import sessionmaker

from app import db
from app.models import Activity, EditableHTML, Role, RoomRequest, User
from ..decorators import admin_required
from .forms import RoomRequestForm, ActivityForm, TransferForm

room_request = Blueprint('room_request', __name__)

@login_required
@room_request.route('/', methods=['GET', 'POST'])
def manage():
    """View all room requests."""
    room_requests = RoomRequest.query.all()
    return render_template('room_request/manage.html', room_requests=room_requests)

@login_required
@room_request.route('/new', methods=['GET', 'POST'])
def new():
    """Room Request page."""
    editable_html_obj = EditableHTML.get_editable_html('room_request')
    form = RoomRequestForm()
    if form.validate_on_submit():
        room_request = RoomRequest(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            relationship_to_patient = form.rel_to_patient.data,
            address_line_one = form.street_address.data,
            address_line_two = form.apt_st_address.data,
            city = form.city.data,
            state = form.state.data,
            zip_code = form.zipcode.data,
            country = form.country.data,
            primary_phone = form.phone_number.data,
            secondary_phone = form.alt_phone_number.data,
            email = form.email.data,
            primary_language = form.primary_language.data,
            secondary_language = form.secondary_language.data,
            previous_stay = form.stayed_before.data,
            patient_first_name = form.patient_first_name.data,
            patient_last_name = form.patient_last_name.data,
            patient_dob = form.patient_dob.data,
            patient_gender = form.patient_gender.data,
            patient_hospital = form.hospital.data,
            patient_hospital_department = form.hospital_dep.data,
            patient_treatment_description = form.description.data,
            patient_diagnosis = form.diagnosis.data,
            patient_first_appt_date = form.first_appt_date.data,
            patient_check_in = form.check_in_date.data,
            patient_check_out = form.check_out_date.data,
            patient_treating_doctor = form.treating_dr.data,
            patient_doctors_phone = form.dr_phone_number.data,
            patient_social_worker = form.hospital_social_worker.data,
            patient_social_worker_phone = form.sw_phone_number.data,
            inpatient = form.in_or_out_patient.data,
            inpatient_prior = form.staying_prior_to_admission.data,
            vaccinated = form.vaccinated.data,
            comments = form.comments.data,
            wheelchair_access = form.wheelchair_access.data,
            full_bathroom = form.full_bathroom.data,
            pack_n_play = form.pack_n_play.data
        )
        db.session.add(room_request)
        db.session.commit()

        from app.email import send_email
        from flask_rq import get_queue
        get_queue().enqueue(
            send_email,
            recipient=room_request.email,
            subject='PRMH Room Request Submitted',
            template='room_request/confirmation_email',
            roomreq=room_request)
        flash('Successfully submitted form', 'form-success')
        return render_template('room_request/new_room_request.html', form=form, editable_html_obj=editable_html_obj)


@login_required
@room_request.route('<int:room_request_id>/delete', methods=['POST'])
def delete_room_request(room_request_id):
    """Request deletion of a user's account."""
    room_request = RoomRequest.query.filter_by(id=room_request_id).first()
    if room_request:
        db.session.delete(room_request)
        db.session.commit()
        flash(f'Successfully deleted room request for {room_request.first_name} {room_request.last_name}.')
    return redirect('/room-request/')


@room_request.route('/<int:form_id>', methods=['GET', 'POST'])
def viewID(form_id):
    form = ActivityForm()
    trasnferf = TransferForm()
    user_found = False
    comments = Activity.query.filter_by(room_request_id = form_id)
    name = ""
    try:
        request_ob = RoomRequest.query.get(form_id)
        print("User found")
        name = str(request_ob.first_name) + " " + str(request_ob.last_name)
        user_found = True
    except: 
        user_found = False
    if form.validate_on_submit():
            activity = Activity(
                text=form.body.data,
                commenter = current_user.first_name,
                user_id = current_user.id,
                room_request_id = request_ob.id
                )
            db.session.add(activity)
            db.session.commit()
            flash("Your comment has been added to the post", 'form-post')
            form.body.data = ''
            return render_template('room_request/id.html', id = form_id, name = name, user_found = user_found,
                                                    transfer= trasnferf, form = form, comments = comments)
    if trasnferf.validate_on_submit():
       flash("Succesfully Trasnfered!")
       return render_template('room_request/id.html', id = form_id, name = name, user_found = user_found,
                                                    transfer= trasnferf, form = form, comments = comments)
    return render_template('room_request/id.html', id = form_id, name = name, user_found = user_found,
                                                    transfer= trasnferf, form = form, comments = comments)
@room_request.route('/<int:form_id>/transfer', methods=['GET', 'POST'])
def transfer(form_id):
    form = TransferForm
    transfered = False
    form_id = form_id
    param_string = "DRIVER={};SERVER={};DATABASE={};UID={};PWD={}".format(
            os.getenv('SQL_SERVER') or "{SQL Server}",
            os.getenv('AZURE_SERVER'),
            os.getenv('AZURE_DATABASE'),
            os.getenv('AZURE_USERNAME'),
            os.getenv('AZURE_PASS'))
    params = urllib.parse.quote_plus(param_string)    
    engine = sqlalchemy.engine.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
    Session = sessionmaker(bind=engine)
    session1 = Session()
    try:
        user = RoomRequest.query.get(form_id)
        name = str(user.first_name) + " " + str(user.last_name)
        try:
            local_object = session1.merge(user)
            session1.add(local_object)
            session1.commit()
            transfered = True
            flash("Room Request Transfered!", 'form-transfer')
            return redirect(url_for('room_request.viewID', form_id = form_id))
        except Exception as e:
            session1.rollback()
            return render_template('room_request/transfer.html', id = form_id, transfered = transfered, error = e)
    except Exception as e:
        print(e)
        return render_template('room_request/transfer.html', id = form_id, transfered = transfered, error = e)


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

