from flask_wtf import FlaskForm, RecaptchaField
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (PasswordField, StringField, SubmitField,
                            IntegerField, BooleanField, FormField, TextAreaField,
                            HiddenField)
from wtforms.fields.html5 import EmailField, TelField, DateField
from wtforms.validators import Email, EqualTo, InputRequired, Length, NumberRange, Optional, Required

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
        'Have you submitted a room request before?')

    # Patient information
    patient_last_name = StringField(
        'Last name', validators=[InputRequired(), Length(1, 128)])
    patient_first_name = StringField(
        'First name', validators=[InputRequired(), Length(1, 128)])
    patient_dob = DateField(
        'Date of Birth', validators=[InputRequired()])
    patient_gender = StringField(
        'Gender', validators=[InputRequired(), Length(1, 64)])
    hospital = StringField(
        'Hospital in Philadelphia', validators=[InputRequired(), Length(1, 128)])
    hospital_department = StringField(
        'Hospital Department (e.g. Oncology, Cardiology, Neonatology)', validators=[InputRequired(), Length(1, 128)])
    description = StringField(
        'Brief Description of Treatment', validators=[InputRequired(), Length(1, 256)])
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
    recaptcha = RecaptchaField()
    submit = SubmitField('Create')


class ActivityForm(FlaskForm):
    body = StringField("Body", validators=[InputRequired()])
    submit = SubmitField("Post")

class TransferForm(FlaskForm):
    transfer = SubmitField("Transfer")
