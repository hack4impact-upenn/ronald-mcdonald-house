from .. import db
from .activity import Activity
from .guest import Guest
from sqlalchemy import Column, Integer, Boolean, DateTime
from datetime import datetime

class RoomRequest(db.Model):
    __tablename__ = "room_requests"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # Requester Personal Information
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    relationship_to_patient = db.Column(db.String(100))
    address_line_one = db.Column(db.String(1000))
    address_line_two = db.Column(db.String(1000))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    zip_code = db.Column(db.String(15))
    country = db.Column(db.String(64))
    primary_phone = db.Column(db.String(50))
    secondary_phone = db.Column(db.String(50))
    email = db.Column(db.String(1000))
    primary_language = db.Column(db.String(100))
    secondary_language = db.Column(db.String(100))
    previous_stay = db.Column(db.Boolean())

    # Patient Information
    patient_first_name = db.Column(db.String(100))
    patient_last_name = db.Column(db.String(100))
    patient_dob = db.Column(db.Date)
    patient_gender = db.Column(db.String(15))
    patient_hospital = db.Column(db.String(1000))
    patient_hospital_department = db.Column(db.String(1000))
    patient_treatment_description = db.Column(db.String(1000))
    patient_diagnosis = db.Column(db.String(1000))
    patient_first_appt_date = db.Column(db.Date)
    patient_check_in = db.Column(db.Date)
    patient_check_out = db.Column(db.Date)
    patient_treating_doctor = db.Column(db.String(100))
    patient_doctors_phone = db.Column(db.String(64))
    patient_social_worker = db.Column(db.String(100))
    patient_social_worker_phone = db.Column(db.String(100))
    inpatient = db.Column(db.String(24))
    inpatient_prior = db.Column(db.Boolean())
    vaccinated = db.Column(db.Boolean())
    comments = db.Column(db.String(5000))

    #Required not on form
    phone_3 = db.Column(db.String(50))
    phone_4 = db.Column(db.String(50))
    email_2 = db.Column(db.String(1000))
    notes = db.Column(db.String(10000))
    regionID = db.Column(db.Integer())
    secondary_regionID = db.Column(db.Integer())
    media_wavier_status = db.Column(db.Integer())
    email_list_status = db.Column(db.Integer())
    email_list_status_2 = db.Column(db.Integer())
    secondary_email_list_status = db.Column(db.Integer())
    secondary_email_list_status2 = db.Column(db.Integer())
    ethnicityID = db.Column(db.Integer())
    primary_languageID = db.Column(db.Integer())
    secondary_languageID = db.Column(db.Integer())
    wheelchair_access_2 = db.Column(db.Integer())
    wheelchair_access_3 = db.Column(db.Integer())
    wheelchair_access_4 = db.Column(db.Integer())
    fee_assistnace = db.Column(db.Integer())
    do_no_mail = db.Column(db.Integer())
    seconard_do_not_mail = db.Column(db.Integer())
    familiy_incomeID = db.Column(db.Integer())
    third_party_transport_approved = db.Column(db.Integer())

    #Optional fields
    patient_death_date = db.Column(db.Date)
    patient_2_first_name = db.Column(db.String(100))
    patient_2_last_name = db.Column(db.String(100))
    patient_2_dob = db.Column(db.Date)
    patient_2_gender = db.Column(db.String(15))
    patient_2_death_date = db.Column(db.Date)
    patient_3_first_name = db.Column(db.String(100))
    patient_3_last_name = db.Column(db.String(100))
    patient_3_dob = db.Column(db.Date)
    patient_3_gender = db.Column(db.String(15))
    patient_3_death_date = db.Column(db.Date)
    patient_4_first_name = db.Column(db.String(100))
    patient_4_last_name = db.Column(db.String(100))
    patient_4_dob = db.Column(db.Date)
    patient_4_gender = db.Column(db.String(15))
    patient_4_death_date = db.Column(db.Date)

    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_relationship = db.Column(db.String(30))
    emergency_contact_phone_1_desc = db.Column(db.String(20))
    emergency_contact_phone_1 = db.Column(db.String(20))
    emergency_contact_phone_2_desc = db.Column(db.String(20))
    emergency_contact_phone_2 = db.Column(db.String(20))
    seconadry_address_line_one = db.Column(db.String(1000))
    seconadry_address_line_two = db.Column(db.String(1000))
    seconadry_city = db.Column(db.String(64))
    seconadry_state = db.Column(db.String(64))
    seconadry_zip_code = db.Column(db.String(10))
    seconadry_country = db.Column(db.String(50))
    seconadry_phone_1_desc = db.Column(db.String(20))
    seconadry_phone_1 = db.Column(db.String(20))
    seconadry_phone_2_desc = db.Column(db.String(20))
    seconadry_phone_2 = db.Column(db.String(20))
    seconadry_phone_3_desc = db.Column(db.String(20))
    seconadry_phone_3 = db.Column(db.String(20))
    seconadry_phone_4_desc = db.Column(db.String(20))
    seconadry_phone_4 = db.Column(db.String(20))
    SecondaryEmailAddress = db.Column(db.String(100))
    SecondaryEmailAddress2 = db.Column(db.String(100))
    SecondaryEmergencyContactName = db.Column(db.String(100))
    SecondaryEmergencyContactRelationship = db.Column(db.String(30))
    SecondaryEmergencyContactPhone1Desc = db.Column(db.String(20))
    SecondaryEmergencyContactPhone1 = db.Column(db.String(20))
    SecondaryEmergencyContactPhone2Desc = db.Column(db.String(20))
    SecondaryEmergencyContactPhone2 = db.Column(db.String(20))
    Patient2MiddleName = db.Column(db.String(100))
    Patient3MiddleName = db.Column(db.String(100))
    Patient4MiddleName = db.Column(db.String(100))
    

    # Special Needs
    wheelchair_access = db.Column(db.Boolean())
    full_bathroom = db.Column(db.Boolean())
    pack_n_play = db.Column(db.Boolean())

    # Relationship
    guests = db.relationship('Guest', backref='room_request')
    activity = db.relationship('Activity', backref='activity')

    def __repr__(self):
        return ('<Room Request \n'
                f'id: {self.id}\n'
                f'First Name: {self.first_name}\n'
                f'Last Name: {self.last_name}\n'
                f'Patient First Name: {self.patient_first_name}\n>'
                f'Patient Last Name: {self.patient_last_name}\n>')

    def __str__(self):
        return self.__repr__()

    def print_info(self):
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
                f'Patient First Name: {self.patient_first_name}\n'
                f'Patient Last Name: {self.patient_last_name}\n'
                f'Patient DOB: {self.patient_dob}\n'
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
                f'Wheelchair Access: {self.wheelchair_access}\n'
                f'Full Bathroom: {self.full_bathroom}\n'
                f'Pack n Play: {self.pack_n_play}\n>')

    @staticmethod
    def generate_fake(count=5, **kwargs):
        """Generate fake room requests for testing."""
        from sqlalchemy.exc import IntegrityError
        from faker import Faker
        from random import seed, choice

        fake = Faker()
        seed()
        for _ in range(count):
            request = RoomRequest(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                relationship_to_patient=choice(["Father", "Mother", "Parent"]),
                address_line_one=fake.street_address(),
                address_line_two=fake.secondary_address(),
                city=fake.city(),
                state=fake.state(),
                zip_code=fake.zipcode(),
                country=fake.country(),
                primary_phone=fake.phone_number(),
                secondary_phone=fake.phone_number(),
                email=fake.email(),
                primary_language=choice(["English", "Spanish"]),
                secondary_language=choice(["English", "Spanish", "Japanese", "ASL"]),
                previous_stay=fake.boolean(),
                patient_first_name=fake.first_name(),
                patient_last_name=fake.last_name(),
                patient_dob=fake.past_date(),
                patient_gender=choice(["Male", "Female", "Non Binary"]),
                patient_hospital=choice(["Children's Hospital of Pennsylvania", "Hospital of the University of Pennsylvania", "St. Christopher's", "Shriners"]),
                patient_hospital_department=choice(["Pediatrics","Oncology","General"]),
                patient_treatment_description=fake.word(),
                patient_diagnosis=fake.word(),
                patient_first_appt_date=fake.future_date(),
                patient_check_in=fake.future_date(),
                patient_check_out=fake.future_date(),
                patient_treating_doctor=fake.name(),
                patient_doctors_phone=fake.phone_number(),
                patient_social_worker=fake.name(),
                patient_social_worker_phone=fake.phone_number(),
                inpatient=choice(['Inpatient', 'Outpatient']),
                inpatient_prior=fake.boolean(),
                vaccinated=fake.boolean(),
                comments=fake.sentence(),
                wheelchair_access=fake.boolean(),
                full_bathroom=fake.boolean(),
                pack_n_play=fake.boolean(),
                **kwargs)
            db.session.add(request)
            try:
                db.session.commit()
                Guest.generate_fake(request)
                Activity.generate_fake(request)
            except IntegrityError:
                db.session.rollback()

    @staticmethod
    def delete(id):
        room_request = RoomRequest.query.get(id)
        if room_request is None:
            print(f"No room request in database with id {id}.")
        else:
            try:
                db.session.delete(room_request)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
