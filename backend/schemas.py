from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class StudentData(BaseModel):
    # ── Personal Details ──────────────────────────────────────────────────────
    name: str = Field(..., min_length=2, description="Full Name")
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    aadhaar_number: Optional[str] = None
    nationality: Optional[str] = None
    religion: Optional[str] = None
    community: Optional[str] = None
    caste: Optional[str] = None

    # ── Contact Details ───────────────────────────────────────────────────────
    mobile_number: Optional[str] = None
    email: Optional[EmailStr] = None
    residential_address: Optional[str] = None
    parent_contact_number: Optional[str] = None

    # ── Parent / Guardian Details ─────────────────────────────────────────────
    father_name: Optional[str] = None
    father_occupation: Optional[str] = None
    mother_name: Optional[str] = None
    mother_occupation: Optional[str] = None
    annual_income: Optional[str] = None
    guardian_name: Optional[str] = None
    guardian_relation: Optional[str] = None

    # ── Academic Details ──────────────────────────────────────────────────────
    registration_number: Optional[str] = None
    previous_school: Optional[str] = None
    board_university: Optional[str] = None
    marks_percentage: Optional[str] = None
    year_of_passing: Optional[str] = None
    tc_number: Optional[str] = None

    # ── Course Details ────────────────────────────────────────────────────────
    course_department: Optional[str] = None
    medium_of_instruction: Optional[str] = None
    admission_category: Optional[str] = None

    # ── Bank Details ──────────────────────────────────────────────────────────
    bank_account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    bank_name: Optional[str] = None

    # ── Other Details ─────────────────────────────────────────────────────────
    hostel_required: Optional[str] = None
    transport_required: Optional[str] = None
    scholarship_details: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_number: Optional[str] = None

    class Config:
        from_attributes = True
