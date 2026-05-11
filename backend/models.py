from sqlalchemy import Column, Integer, String, Text
from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    # ── Personal Details ──────────────────────────────────────────────────────
    name = Column(String, index=True)
    date_of_birth = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    blood_group = Column(String, nullable=True)
    aadhaar_number = Column(String, nullable=True, unique=True)
    nationality = Column(String, nullable=True)
    religion = Column(String, nullable=True)
    community = Column(String, nullable=True)
    caste = Column(String, nullable=True)

    # ── Contact Details ───────────────────────────────────────────────────────
    mobile_number = Column(String, nullable=True)
    email = Column(String, nullable=True, unique=True, index=True)
    residential_address = Column(Text, nullable=True)
    parent_contact_number = Column(String, nullable=True)

    # ── Parent / Guardian Details ─────────────────────────────────────────────
    father_name = Column(String, nullable=True)
    father_occupation = Column(String, nullable=True)
    mother_name = Column(String, nullable=True)
    mother_occupation = Column(String, nullable=True)
    annual_income = Column(String, nullable=True)
    guardian_name = Column(String, nullable=True)
    guardian_relation = Column(String, nullable=True)

    # ── Academic Details ──────────────────────────────────────────────────────
    registration_number = Column(String, nullable=True, unique=True, index=True)
    previous_school = Column(String, nullable=True)
    board_university = Column(String, nullable=True)
    marks_percentage = Column(String, nullable=True)
    year_of_passing = Column(String, nullable=True)
    tc_number = Column(String, nullable=True)

    # ── Course Details ────────────────────────────────────────────────────────
    course_department = Column(String, nullable=True)
    medium_of_instruction = Column(String, nullable=True)
    admission_category = Column(String, nullable=True)

    # ── Bank Details ──────────────────────────────────────────────────────────
    bank_account_number = Column(String, nullable=True)
    ifsc_code = Column(String, nullable=True)
    bank_name = Column(String, nullable=True)

    # ── Other Details ─────────────────────────────────────────────────────────
    hostel_required = Column(String, nullable=True)
    transport_required = Column(String, nullable=True)
    scholarship_details = Column(Text, nullable=True)
    emergency_contact_name = Column(String, nullable=True)
    emergency_contact_number = Column(String, nullable=True)
