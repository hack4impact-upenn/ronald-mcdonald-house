from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (PasswordField, StringField, SubmitField,
                            IntegerField, BooleanField, FormField, TextAreaField,
                            HiddenField)
from wtforms.fields.html5 import EmailField, TelField, DateField
from ..custom_fields import CustomModelSelectField, HospitalListField
from wtforms.validators import Email, EqualTo, InputRequired, Length, NumberRange, Optional
from ..models import Hospital, RoomRequest


class RoomRequestForm(FlaskForm):
    # Personal information of requester
    first_name = StringField(
        'First name', validators=[InputRequired(), Length(1, 64)])
    last_name = StringField(
        'Last name', validators=[InputRequired(), Length(1, 64)])
    rel_to_patient = StringField(
        'Relationship to Patient', validators=[InputRequired(), Length(1, 64)])
    street_address = StringField(
        'Street Address', validators=[InputRequired()])
    apt_st_address = StringField(
        'Apt/Suite Address')
    city = StringField(
        'City', validators=[InputRequired()])
    state = StringField(
        'State', validators=[InputRequired()])
    zipcode = StringField(
        'Zipcode', validators=[InputRequired()])
    country = StringField(
        'Country', validators=[InputRequired()])
    phone_number = TelField(
        'Phone Number', validators=[InputRequired()])
    alt_phone_number = TelField(
        'Alternate Phone Number', validators=[InputRequired()])
    email = EmailField(
        'Email', validators=[InputRequired(), Length(1, 64), Email()])
    primary_language = StringField(
        'Primary Language', validators=[Length(1, 128)])
    secondary_language = StringField(
        'Secondary Language', validators=[Length(0, 128)])
    stayed_before = BooleanField(
        'Have you stayed at PRMH before?')

    # Patient information
    patient_last_name = StringField(
        'Last name', validators=[InputRequired(), Length(1, 128)])
    patient_first_name = StringField(
        'First name', validators=[InputRequired(), Length(1, 128)])
    patient_dob = DateField(
        'Date of Birth', validators=[InputRequired()])
    patient_gender = StringField(
        'Gender', validators=[InputRequired(), Length(1, 64)])
    hospital = CustomModelSelectField(
        label='Hospital in Philadelphia',
        validators=[InputRequired()],
        model=Hospital,
        order_column='name')
    other_hospital = StringField(
        'If you selected "Other," please indicate the hospital name.',
        validators=[Optional(), Length(1, 500)])
    hospital_department = StringField(
        'Hospital Department (e.g. Oncology, Cardiology, Neonatology)', validators=[InputRequired(), Length(1, 128)])
    description = StringField(
        'Brief Description of Treatment', validators=[InputRequired(), Length(1, 1000)])
    diagnosis = StringField(
        'Diagnosis', validators=[InputRequired(), Length(1, 256)])
    first_appt_date = DateField(
        'Date of First Appointment During Requested Stay', validators=[InputRequired()])
    check_in_date = DateField(
        'Check In', validators=[InputRequired()])
    check_out_date = DateField(
        'Check Out', validators=[InputRequired()])
    treating_doctor = StringField(
        'Treating Doctor', validators=[InputRequired(), Length(1, 128)])
    doctor_phone_number = TelField(
        "Doctor's Phone Number")
    hospital_social_worker = StringField(
        'Hospital Social Worker', validators=[Length(1, 128)])
    sw_phone_number = TelField(
        "Hospital Social Worker's Phone Number")
    in_or_out_patient = StringField(
        'Inpatient/Outpatient', validators=[InputRequired(), Length(1, 128)])
    staying_prior_to_admission = BooleanField(
        'For Inpatient Only: Will the patient be staying in the House prior to admission? (Explain in the Comments section below)')
    vaccinated = BooleanField(
        'Have all patients and family members who will be staying at the House been vaccinated for measles, mumps, and rubella (MMR), and been vaccinated for and/or diagnosed with chickenpox in the past?')
    comments = TextAreaField('Comments', validators=[Length(0, 3000)])

    # Room occupancy
    guest1_name = StringField(
        'Guest name', validators=[InputRequired(), Length(1, 128)])
    guest1_dob = DateField(
        'Guest Date of Birth', validators=[InputRequired()])
    guest1_rel_to_patient = StringField(
        'Relationship to Patient', validators=[InputRequired(), Length(1, 64)])
    guest1_email = EmailField(
        'Email', validators=[InputRequired(), Length(1, 64), Email()])
    guest1_guardian = BooleanField('Guardian?')

    guest2_name = StringField(
        'Guest name', validators=[Optional(), Length(1, 128)])
    guest2_dob = DateField(
        'Guest Date of Birth', validators=[Optional()])
    guest2_rel_to_patient = StringField(
        'Relationship to Patient', validators=[Optional(), Length(1, 64)])
    guest2_email = EmailField(
        'Email', validators=[Optional(), Length(1, 64), Email()])
    guest2_guardian = BooleanField('Guardian?')

    guest3_name = StringField(
        'Guest name', validators=[Optional(), Length(1, 128)])
    guest3_dob = DateField(
        'Guest Date of Birth', validators=[Optional()])
    guest3_rel_to_patient = StringField(
        'Relationship to Patient', validators=[Optional(), Length(1, 64)])
    guest3_email = EmailField(
        'Email', validators=[Optional(), Length(1, 64), Email()])
    guest3_guardian = BooleanField('Guardian?')

    guest4_name = StringField(
        'Guest name', validators=[Optional(), Length(1, 128)])
    guest4_dob = DateField(
        'Guest Date of Birth', validators=[Optional()])
    guest4_rel_to_patient = StringField(
        'Relationship to Patient', validators=[Optional(), Length(1, 64)])
    guest4_email = EmailField(
        'Email', validators=[Optional(), Length(1, 64), Email()])
    guest4_guardian = BooleanField('Guardian?')

    guest5_name = StringField(
        'Guest name', validators=[Optional(), Length(1, 128)])
    guest5_dob = DateField(
        'Guest Date of Birth', validators=[Optional()])
    guest5_rel_to_patient = StringField(
        'Relationship to Patient', validators=[Optional(), Length(1, 64)])
    guest5_email = EmailField(
        'Email', validators=[Optional(), Length(1, 64), Email()])
    guest5_guardian = BooleanField('Guardian?')

    # Special needs
    wheelchair_access = BooleanField('Wheelchair Access')
    full_bathroom = BooleanField('Full Bathroom with Tub')
    pack_n_play = BooleanField("Pack 'N' Play")
    
    submit = SubmitField('Create')

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        elif self.hospital.data == 'other' and self.other_hospital.data == '':
            self.other_hospital.errors.append('This field is required.')
        return True

class HospitalForm(FlaskForm):
    hospitals = HospitalListField('', description="Please enter each hospital on a separate line.")
    submit = SubmitField('Save')

class ActivityForm(FlaskForm):
    body = StringField("Body", validators=[InputRequired()])
    submit = SubmitField("Post")

class TransferForm(FlaskForm):
    transfer = SubmitField("Transfer")


def get_room_request_from_form(form):
    """Returns a room request from the given submitted RoomRequestForm."""
    hospital = form.other_hospital.data if form.hospital.data == 'other' else form.hospital.data
    room_request = RoomRequest(
        first_name=form.first_name.data,
        last_name=form.last_name.data,
        relationship_to_patient=form.rel_to_patient.data,
        address_line_one=form.street_address.data,
        address_line_two=form.apt_st_address.data,
        city=form.city.data,
        state=form.state.data,
        zip_code=form.zipcode.data,
        country=form.country.data,
        primary_phone=form.phone_number.data,
        secondary_phone=form.alt_phone_number.data,
        email=form.email.data,
        primary_language=form.primary_language.data,
        secondary_language=form.secondary_language.data,
        previous_stay=form.stayed_before.data,
        patient_first_name=form.patient_first_name.data,
        patient_last_name=form.patient_last_name.data,
        patient_dob=form.patient_dob.data,
        patient_gender=form.patient_gender.data,
        patient_hospital=hospital,
        patient_hospital_department=form.hospital_department.data,
        patient_treatment_description=form.description.data,
        patient_diagnosis=form.diagnosis.data,
        patient_first_appt_date=form.first_appt_date.data,
        patient_check_in=form.check_in_date.data,
        patient_check_out=form.check_out_date.data,
        patient_treating_doctor=form.treating_doctor.data,
        patient_doctors_phone=form.doctor_phone_number.data,
        patient_social_worker=form.hospital_social_worker.data,
        patient_social_worker_phone=form.sw_phone_number.data,
        inpatient=form.in_or_out_patient.data,
        inpatient_prior=form.staying_prior_to_admission.data,
        vaccinated=form.vaccinated.data,
        comments=form.comments.data,
        wheelchair_access=form.wheelchair_access.data,
        full_bathroom=form.full_bathroom.data,
        pack_n_play=form.pack_n_play.data)
    
    guests = []
    for i in range(1, 6):
        guest_name = form[f'guest{i}_name'].data
        guest_dob = form[f'guest{i}_dob'].data
        guest_rel = form[f'guest{i}_rel_to_patient'].data
        guest_email = form[f'guest{i}_email'].data
        guest_guardian = form[f'guest{i}_guardian'].data
        if guest_name and guest_dob and guest_rel and guest_email and guest_guardian:
            guests.append(Guest(
                name=guest_name,
                dob=guest_dob,
                relationship_to_patient=guest_rel,
                email=guest_email,
                guardian=guest_guardian))
    room_request.guests = guests

    return room_request

def get_form_from_room_request(room_request):
    """Returns a RoomRequestForm with pre-filled data from the given room request."""
    form = RoomRequestForm(
        first_name=room_request.first_name,
        last_name=room_request.last_name,
        rel_to_patient=room_request.relationship_to_patient,
        street_address=room_request.address_line_one,
        apt_st_address=room_request.address_line_two,
        city=room_request.city,
        state=room_request.state,
        zipcode=room_request.zip_code,
        country=room_request.country,
        phone_number=room_request.primary_phone,
        alt_phone_number=room_request.secondary_phone,
        email=room_request.email,
        primary_language=room_request.primary_language,
        secondary_language=room_request.secondary_language,
        stayed_before=room_request.previous_stay,
        patient_first_name=room_request.patient_first_name,
        patient_last_name=room_request.patient_last_name,
        patient_dob=room_request.patient_dob,
        patient_gender=room_request.patient_gender,
        hospital=room_request.patient_hospital,
        hospital_department=room_request.patient_hospital_department,
        description=room_request.patient_treatment_description,
        diagnosis=room_request.patient_diagnosis,
        first_appt_date=room_request.patient_first_appt_date,
        check_in_date=room_request.patient_check_in,
        check_out_date=room_request.patient_check_out,
        treating_doctor=room_request.patient_treating_doctor,
        doctor_phone_number=room_request.patient_doctors_phone,
        hospital_social_worker=room_request.patient_social_worker,
        sw_phone_number=room_request.patient_social_worker_phone,
        in_or_out_patient=room_request.inpatient,
        staying_prior_to_admission=room_request.inpatient_prior,
        vaccinated=room_request.vaccinated,
        comments=room_request.comments,
        wheelchair_access=room_request.wheelchair_access,
        full_bathroom=room_request.full_bathroom,
        pack_n_play=room_request.pack_n_play)

    for i, guest in enumerate(room_request.guests):
        form[f'guest{i+1}_name'].data = guest.name
        form[f'guest{i+1}_dob'].data = guest.dob
        form[f'guest{i+1}_rel_to_patient'].data = guest.relationship_to_patient
        form[f'guest{i+1}_email'].data = guest.email
        form[f'guest{i+1}_guardian'].data = guest.guardian

    return form