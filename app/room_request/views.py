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
from sqlalchemy import *


from .forms import RoomRequestForm, ActivityForm, TransferForm
from .helpers import get_room_request_from_form, get_form_from_room_request
from ..decorators import admin_required
from ..email import send_email
from ..models import Activity, EditableHTML, RoomRequest, Guest, User, Role

room_request = Blueprint('room_request', __name__)

@room_request.route('/')
@login_required
def index():
    """View all room requests."""
    room_requests = RoomRequest.query.all()
    return render_template('admin/index.html', room_requests=room_requests)


@room_request.route('/<int:id>/manage')
@room_request.route('/<int:id>/info')
@login_required
def manage(id):
    """Manage room request."""
    room_request = RoomRequest.query.get(id)
    if room_request is None:
        return abort(404)
    return render_template('room_request/manage.html', room_request=room_request)


@room_request.route('/<int:id>/patient')
@login_required
def patient_info(id):
    """View patient info of given room request."""
    room_request = RoomRequest.query.get(id)
    if room_request is None:
        return abort(404)
    return render_template('room_request/manage.html', room_request=room_request)


@room_request.route('/<int:id>/room-occupancy')
@login_required
def room_occupancy_info(id):
    """View room occupancy needs for given room request."""
    room_request = RoomRequest.query.get(id)
    if room_request is None:
        return abort(404)
    return render_template('room_request/manage.html', room_request=room_request)


@room_request.route('/<int:id>/guests')
@login_required
def guest_info(id):
    """View table of guests for given room request."""
    room_request = RoomRequest.query.get(id)
    if room_request is None:
        return abort(404)
    return render_template('room_request/manage.html', room_request=room_request)

@room_request.route('/<int:id>/comments', methods=['GET', 'POST'])
@login_required
def comments(id):    
    room_request = RoomRequest.query.get(id)
    if room_request is None:
        return abort(404)

    comments_all = Activity.query.filter_by(room_request_id=id)
    activity_form = ActivityForm()

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

    return render_template('room_request/manage.html',
        id=id,
        room_request=room_request,
        activity_form=activity_form,
        comments_all=comments_all)

@room_request.route('/<int:id>/edit')
@login_required
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


@room_request.route('<int:id>/delete')
@login_required
def delete(id):
    """Request deletion of a room request, but does not actually perform the action until user confirmation."""
    room_request = RoomRequest.query.get(id)
    if room_request is None:
        return abort(404)
    return render_template('room_request/manage.html', room_request=room_request)


@room_request.route('<int:id>/_delete')
@login_required
def _delete(id):
    """Delete a room request."""
    room_request = RoomRequest.query.get(id)
    if room_request:
        db.session.delete(room_request)
        db.session.commit()
        flash(f'Successfully deleted room request for {room_request.first_name} {room_request.last_name}.', 'success')
    return redirect(url_for('admin.index'))


@room_request.route('/new', methods=['GET', 'POST'])
def new():
    """Room Request page."""
    editable_html_obj = EditableHTML.get_editable_html('room_request')
    form = RoomRequestForm(request.form)
    if form.is_submitted() and not form.validate_on_submit():
        flash('Please check the reCaptcha at the bottom of the page.', 'form-error')
    elif form.validate_on_submit():
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
            flash('Successfully submitted form', 'form-success')
        except IntegrityError:
            db.session.rollback()
            flash('Unable to save changes. Please try again.', 'form-error')
    return render_template('room_request/new.html', form=form, editable_html_obj=editable_html_obj)
    

@room_request.route('/<int:id>', methods=['GET', 'POST'])
@login_required
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

    return render_template('room_request/manage.html',
        id=id,
        room_request=room_request,
        activity_form=activity_form,
        transfer_form=transfer_form,
        comments=comments)


@room_request.route('/<int:id>/transfer', methods=['GET', 'POST'])
@login_required
def transfer(id):
    room_request = RoomRequest.query.get(id)
    if room_request is None:
        return abort(404)

    transferred = False
    param_string = "DRIVER={};SERVER={};DATABASE={};UID={};PWD={}".format(
            os.getenv('SQL_SERVER') or "{ODBC Driver 17 for SQL Server}",
            os.getenv('AZURE_SERVER'),
            os.getenv('AZURE_DATABASE'),
            os.getenv('AZURE_USERNAME'),
            os.getenv('AZURE_PASS'))    
    params = urllib.parse.quote_plus(param_string)    
    engine = sqlalchemy.engine.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
    session = sessionmaker(bind=engine)()
    metadata = MetaData(bind=engine)

    family = Table('Family', metadata, autoload=True)
    familyMember = Table('FamilyMember', metadata, autoload=True)
    familyWaitList = Table('FamilyWaitList', metadata, autoload=True)
    supRelationship = Table('supRelationship', metadata, autoload=True)
    supHospital = Table('supHospital', metadata, autoload=True)
    supWard = Table('supWard', metadata, autoload=True)
    supDiagnosis = Table('supDiagnosis', metadata, autoload=True)
    supReasonForVisit = Table('supReasonForVisit', metadata, autoload=True)
    wheelchair = 0
    if room_request.wheelchair_access:
        wheelchair = 1
    try:
        insFam = family.insert().values(PatientSurname= room_request.patient_last_name, PatientFirstName= room_request.patient_first_name, PatientGender= room_request.patient_gender[0], PatientBirthDate = room_request.patient_dob, Address = (room_request.address_line_one + " " + room_request.address_line_two), City = room_request.city, ProvinceCode = room_request.state[0:3], PostalCode = room_request.zip_code, Country = room_request.country, Phone1Desc = "Phone 1", Phone1 = room_request.primary_phone, Phone2Desc = "Phone 2", Phone2 = room_request.secondary_phone, Phone3Desc = "", Phone3 = "", Phone4Desc = "", Phone4 = "", EmailAddress = "",  EmailAddress2 = "", DateCreated = room_request.created_at, CreatedBy = "Web Form", DateModified = room_request.created_at, ModifiedBy = "Web Form",  PatientRequiresWheelchair = wheelchair)
        conn = engine.connect()
        famResult = conn.execute(insFam)
        famEntry = family.select().execute().fetchone()
        famID = famEntry.FamilyID
        relationshipID = engine.execute("""SELECT ISNULL(
        (
         SELECT [supRelationship].[RelationshipID] 
         FROM [supRelationship]
         WHERE [supRelationship].[RelationshipDesc] = {}
        ), 1)""".format("\'" + room_request.relationship_to_patient.replace("'","''") + "\'"))
        relationshipID = relationshipID.first()[0]
        insFamMember = familyMember.insert().values(FamilyID = famID, Surname = room_request.last_name, FirstName = room_request.first_name, MiddleNames = '', BirthDate = '', Gender = '', RelationshipID = relationshipID, DateCreated = room_request.created_at, CreatedBy = 'Web Form', DateModified = room_request.created_at, ModifiedBy = 'Web Form', Notes = '')
        famMemberResult = conn.execute(insFamMember)
        for guest in room_request.guests:
            guard = 0
            if guest.guardian:
                guard = 1
            lastName = str(guest.name.split(' ')[1])
            firstName = str(guest.name.split(' ')[0])
            relationshipID = engine.execute("""SELECT ISNULL(
            (
            SELECT [supRelationship].[RelationshipID] 
            FROM [supRelationship]
            WHERE [supRelationship].[RelationshipDesc] = {}
            ), 1)""".format("\'" + room_request.relationship_to_patient.replace("'","''") + "\'"))
            relationshipID = relationshipID.first()[0]
            insFamMember = familyMember.insert().values(FamilyID = famID, Surname = lastName, FirstName = firstName, MiddleNames = '', BirthDate = guest.dob, Gender = '', RelationshipID = relationshipID, DateCreated = room_request.created_at, CreatedBy = 'Web Form', DateModified = room_request.created_at, ModifiedBy = 'Web Form', Notes = '', FirstCaregiver = guard)
            conn.execute(insFamMember)
        hospitalID = engine.execute("""SELECT ISNULL(
        (
         SELECT [supHospital].[HospitalID] 
         FROM [supHospital]
         WHERE [supHospital].[HospitalDesc] = {}
        ), 1)""".format("\'" + room_request.patient_hospital.replace("'","''") + "\'"))
        hospitalID = hospitalID.first()[0]
        wardID = engine.execute("""SELECT ISNULL(
        (
         SELECT [supWard].[WardID] 
         FROM [supWard]
         WHERE [supWard].[WardDesc] = {}
        ), 1)""".format("\'" + room_request.patient_hospital_department.replace("'","''") + "\'"))
        wardID = wardID.first()[0]
        reasonForVisitID = engine.execute("""SELECT ISNULL(
        (
         SELECT [supReasonForVisit].[ReasonForVisitID] 
         FROM [supReasonForVisit]
         WHERE [supReasonForVisit].[ReasonForVisitDesc] = {}
        ), 1)""".format("\'" + room_request.patient_treatment_description.replace("'","''") + "\'"))
        reasonForVisitID = reasonForVisitID.first()[0]
        DiagnosisID = engine.execute("""SELECT ISNULL(
        (
         SELECT [supDiagnosis].[DiagnosisID] 
         FROM [supDiagnosis]
         WHERE [supDiagnosis].[DiagnosisDesc] = {}
        ), 1)""".format("\'" + room_request.patient_diagnosis.replace("'","''") + "\'"))
        DiagnosisID = DiagnosisID.first()[0]
        estimatedLengthOfStay = room_request.patient_check_out - room_request.patient_check_in
        otherReq = ''
        if room_request.full_bathroom:
            otherReq += "Full bathroom requested. "
        if room_request.pack_n_play:
            otherReq += "Pack n play requested. "
        insFamWaitList = familyWaitList.insert().values(FamilyID = famID, StartDate = room_request.patient_check_in, EndDate = room_request.patient_check_out, EndReasonID = 1, DiagnosisID = DiagnosisID, WardID = wardID, TentativeRoomID = 6, EstimatedLengthOfStay = estimatedLengthOfStay.days, ReferralName = '', ReferralOrganization = '', ReferralPhone1Desc = '', ReferralPhone1 = '', ReferralPhone1Ext = '', ReferralPhone2Desc = '', ReferralPhone2 = '', ReferralPhone2Ext = '', ReminderToConfirmGiven = 0, AskedAboutDiseaseSymptoms = 0, OutsideAgencyName = '', OutsideAgencyAddress = '', OutsideAgencyCity = '', OutsideAgencyProvinceCode = '', OutsideAgencyPostalCode = '', OutsideAgencyCountry = '', OutsideAgencyPhone1Desc = '', OutsideAgencyPhone1 = '', OutsideAgencyPhone2Desc = '', OutsideAgencyPhone2 = '', DateCreated = room_request.created_at, CreatedBy = 'Web Form', DateModified = room_request.created_at, ModifiedBy = 'Web Form', DateRequested = room_request.created_at, OtherSpecialRequests = otherReq, HospitalID = hospitalID)
        famWaitListResult = conn.execute(insFamWaitList)
        transferred = True
        flash('Room request succesfully transferred!', 'form-transfer')
        return redirect(url_for('admin.index'))
    except Exception as e:
        session.rollback()
        return render_template('room_request/transfer.html', id=id, transferred=transferred, error=e)


@room_request.route('/<int:id>/duplicates', methods=['GET', 'POST'])
@login_required
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
        .all()
    return render_template('room_request/duplicates.html', duplicate_room_requests=duplicate_room_requests)

