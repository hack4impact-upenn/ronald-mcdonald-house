from flask import (
    Blueprint,
    render_template,
    flash
)

import os
import urllib
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .forms import RoomRequestForm
from ..models import RoomRequest
from app import db
from app.models import EditableHTML, Role, User

room_request = Blueprint('room_request', __name__)

# TODO dashboard at route /

# TODO create form at route /new
@room_request.route('/new', methods=['GET', 'POST'])
def new():
    """Room Request page."""
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

            patient_full_name = form.patient_full_name.data,
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

            #waiting for guest model stuff to upload guests from form
            wheelchair_access = form.wheelchair_access.data,
            full_bathroom = form.full_bathroom.data,
            pack_n_play = form.pack_n_play.data
        )
        db.session.add(room_request)
        db.session.commit()
        flash('Successfully submitted form', 'form-success')
    return render_template('room_request/new_room_request.html', form=form)

    
@room_request.route('/<int:form_id>', methods=['GET', 'POST'])
def viewID(form_id):
    user_found = "false"
    name = ""
    try:
        user = User.query.get(form_id)
        print("User found")
        name = str(user.first_name) + " " + str(user.last_name)
        user_found = "true"
        return render_template('room_request/id.html', id = form_id, name = name, user_found = user_found)
    except: 
        return render_template('room_request/id.html', id = form_id, name = name, user_found = user_found)

@room_request.route('/<int:form_id>/transfer', methods=['GET', 'POST'])
def transfer(form_id):
    transfered = False
    form_id = form_id
    e = ""
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
        user = User.query.get(form_id)
        print(type(user))
        #try:
        local_object = session1.merge(user)
        session1.add(local_object)
        #session1.add(user)
        session1.commit()
        transfered = True
        #except:
            #session.rollback()
    except Exception as e:
        print(e)
        print("failed")
        #flash('User {} successfully transfered'.format(str(e)))

    return render_template('room_request/transfer.html', id = form_id, transfered = transfered)
