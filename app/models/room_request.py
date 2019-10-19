from .. import db
from sqlalchemy import Column, Integer, Boolean
import datetime

class RoomRequest(db.Model):
    __tablename__ = "room_request"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime())

    // Requester Personal Information
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    relationship_to_patient = db.Column(db.String(100))
    address_line_one = db.Column(db.String(1000))
    address_line_two = db.Column(db.String(1000))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    zip_code = db.Column(db.String(15))
    country = db.Column(db.String(64))
    primary_phone = db.Column(db.String(15))
    secondary_phone = db.Column(db.String(15))
    email = db.Column(db.String(1000))
    primary_language = db.Column(db.String(100))
    secondary_language = db.Column(db.String(100))
    previous_stay = db.Column(db.Boolean())

    // Patient Information
    patient_full_name = db.Column(db.String(200))
    patient_dob_month = db.Column(db.Integer())
    patient_dob_day = db.Column(db.Integer())
    patient_dob_year = db.Column(db.Integer())
    patient_gender = db.Column(db.String(15))
    patient_hospital = db.Column(db.String(1000))
    patient_hospital_department = db.Column(db.String(1000))
    patient_treatment_description = db.Column(db.String(1000))
    patient_diagnosis = db.Column(db.String(1000))
    patient_first_appt_date = db.Column(db.String(100))
    patient_check_in = db.Column(db.DateTime())
    patient_check_out = db.Column(db.DateTime())
    patient_treating_doctor = db.Column(db.String(100))
    patient_doctors_phone = db.Column(db.String(64))
    patient_social_worker = db.Column(db.String(100))
    patient_social_worker_phone = db.Column(db.String(100))
    inpatient = db.Column(db.Boolean())
    inpatient_prior = db.Column(db.Boolean())
    vaccinated = db.Column(db.Boolean())
    not_vaccinated_reason = db.Column(db.String(1000))
    comments = db.Column(db.Column(db.String(5000)))

    // Room Request
    room_occupancy = db.relationship('Guest')
    wheelchair_access = db.Column(db.Boolean())
    full_bathroom = db.Column(db.Boolean())
    pack_n_play = db.Column(db.Boolean())

    def __repr__(self):
        return ('<Room Request \n'
                f'Created At: {self.created_at}\n'
                f'First Name: {self.first_name}\n'
                f'Last Name: {self.last_name}\n'
                f'Relationship to Patient: {self.relationship_to_patient}\n'
                f'Address Line One: {self.address_line_one}\n'
                f'Address Line Two: {self.address_line_two}\n'
                f'City: {self.city}\n'
                f'State: {self.state}\n'
                f'Zip Code: {self.zip_code}\n'
                f'Country: {self.country}\n'
                f'Primary Phone: {self.primary_phone}\n'
                f'Secondary Phone: {self.secondary_phone}\n'
                f'Email: {self.email}\n'
                f'Primary Language: {self.primary_language}\n'
                f'Secondary Language: {self.secondary_language}\n'
                f'Previous Stay: {self.previous_stay}\n'
                f'Patient Full Name: {self.patient_full_name}\n'
                f'Patient DOB Month: {self.patient_dob_month}\n'
                f'Patient DOB Day: {self.patient_dob_day}\n'
                f'Patient DOB Year: {self.patient_dob_year}\n'
                f'Patient Gender: {self.patient_gender}\n'
                f'Patient Hospital: {self.patient_hospital}\n'
                f'Patient Hospital Department: {self.patient_hospital_department}\n'
                f'Patient Treatment Desciption: {self.patient_treatment_description}\n'
                f'Patient Diagnosis: {self.patient_diagnosis}\n'
                f'Patient First Appointment Date: {self.patient_first_appt_date}\n'
                f'Patient Check In: {self.patient_check_in}\n'
                f'Patient Check Out: {self.patient_check_out}\n'
                f'Patient Treating Doctor: {self.patient_treating_doctor}\n'
                f'Patient Doctor Phone Number: {self.patient_doctors_phone}\n'
                f'Patient Social Worker: {self.patient_social_worker}\n'
                f'Patient Social Worker Phone Number: {self.patient_social_worker_phone}\n'
                f'Inpatient: {self.inpatient}\n'
                f'Inpatient Staying In House Prior: {self.inpatient_prior}\n'
                f'Vaccinated: {self.vaccinated}\n'
                f'Not Vaccinated Reason: {self.not_vaccinated_reason}\n'
                f'Comments: {self.comments}\n'
                f'Room Occupancy: {self.room_occupancy}\n'
                f'Wheelchair Access: {self.wheelchair_access}\n'
                f'Full Bathroom: {self.full_bathroom}\n'
                f'Pack n Play: {self.pack_n_play}\n>')

    def __str__(self):
        return self.__repr__()



class Guest(db.Model):
    # TODO
    pass