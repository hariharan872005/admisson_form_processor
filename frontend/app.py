import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Admission Form Processor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #0f1117; }
[data-testid="stSidebar"] { background: #161b27; border-right: 1px solid #2a2f3e; }

.header-banner {
    background: linear-gradient(135deg, #1a237e 0%, #283593 50%, #1565c0 100%);
    border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 1.5rem;
    display: flex; align-items: center; gap: 1.2rem;
    box-shadow: 0 4px 24px rgba(21,101,192,0.3);
}
.header-banner h1 { margin:0; font-size:2rem; font-weight:700; color:#fff; }
.header-banner p  { margin:.3rem 0 0; color:#90caf9; font-size:.95rem; }

.section-card {
    background: #161b27; border: 1px solid #2a2f3e;
    border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 1rem;
}
.section-title {
    font-size: .8rem; font-weight: 700; color: #42a5f5;
    text-transform: uppercase; letter-spacing: 1px;
    margin-bottom: .8rem; padding-bottom: .4rem;
    border-bottom: 1px solid #2a2f3e;
}
.stat-row { display:flex; gap:1rem; margin-bottom:1.5rem; flex-wrap:wrap; }
.stat-card {
    flex:1; min-width:120px; background:#161b27;
    border:1px solid #2a2f3e; border-radius:12px;
    padding:1rem 1.2rem; text-align:center;
}
.stat-card .num { font-size:1.8rem; font-weight:700; color:#42a5f5; }
.stat-card .lbl { font-size:.75rem; color:#8892a4; text-transform:uppercase; letter-spacing:.5px; }
.info-box {
    background:#0d1b2e; border-left:4px solid #1565c0;
    border-radius:0 8px 8px 0; padding:.8rem 1rem;
    margin:.8rem 0; font-size:.88rem; color:#90caf9;
}
.upload-hint {
    background:#161b27; border:2px dashed #2a2f3e;
    border-radius:12px; padding:1.5rem; text-align:center;
    color:#8892a4; font-size:.9rem; margin-bottom:1rem;
}
.stButton > button { border-radius:8px; font-weight:600; }
[data-testid="stTabs"] [role="tab"] { font-weight:600; font-size:.9rem; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in [("valid_data", None), ("errors", []), ("last_export", None),
              ("processed", False)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 Admission Processor")
    st.markdown("---")
    page = st.radio("", ["📤 Process Forms", "🗄️ View Database", "ℹ️ Help"],
                    label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**Supported Formats**")
    for f, d in [("📄 PDF","Admission forms"),("📝 DOCX","Word documents"),
                 ("📊 CSV","Spreadsheet exports"),("📈 Excel","XLSX workbooks")]:
        st.markdown(f"**{f}** — {d}")
    st.markdown("---")
    try:
        r = requests.get(f"{API_URL}/students", timeout=2)
        total = len(r.json()) if r.status_code == 200 else "?"
        st.success(f"✅ Backend online  •  {total} records")
    except Exception:
        st.error("❌ Backend offline")
        st.caption("Run: uvicorn main:app --reload")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
  <div style="font-size:2.8rem">🎓</div>
  <div>
    <h1>Admission Form Processor</h1>
    <p>Upload PDF, DOCX, CSV or Excel admission forms — extract, validate and export student records.</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═════════════════════════════════════════════════════════════════════════════

FIELD_LABELS = {
    # Personal
    "name": "Full Name", "date_of_birth": "Date of Birth", "gender": "Gender",
    "blood_group": "Blood Group", "aadhaar_number": "Aadhaar Number",
    "nationality": "Nationality", "religion": "Religion",
    "community": "Community", "caste": "Caste",
    # Contact
    "mobile_number": "Mobile Number", "email": "Email ID",
    "residential_address": "Residential Address",
    "parent_contact_number": "Parent's Contact Number",
    # Parent / Guardian
    "father_name": "Father's Name", "father_occupation": "Father's Occupation",
    "mother_name": "Mother's Name", "mother_occupation": "Mother's Occupation",
    "annual_income": "Annual Income", "guardian_name": "Guardian Name",
    "guardian_relation": "Guardian Relation",
    # Academic
    "registration_number": "Registration Number",
    "previous_school": "Previous School / College",
    "board_university": "Board / University",
    "marks_percentage": "Marks / Percentage / CGPA",
    "year_of_passing": "Year of Passing", "tc_number": "TC Number",
    # Course
    "course_department": "Course / Department",
    "medium_of_instruction": "Medium of Instruction",
    "admission_category": "Admission Category",
    # Bank
    "bank_account_number": "Bank Account Number",
    "ifsc_code": "IFSC Code", "bank_name": "Bank Name",
    # Other
    "hostel_required": "Hostel Required",
    "transport_required": "Transport Required",
    "scholarship_details": "Scholarship Details",
    "emergency_contact_name": "Emergency Contact Name",
    "emergency_contact_number": "Emergency Contact Number",
}

SECTIONS = {
    "👤 Personal Details": [
        "name","date_of_birth","gender","blood_group","aadhaar_number",
        "nationality","religion","community","caste"
    ],
    "📞 Contact Details": [
        "mobile_number","email","residential_address","parent_contact_number"
    ],
    "👨‍👩‍👧 Parent / Guardian Details": [
        "father_name","father_occupation","mother_name","mother_occupation",
        "annual_income","guardian_name","guardian_relation"
    ],
    "🎓 Academic Details": [
        "registration_number","previous_school","board_university",
        "marks_percentage","year_of_passing","tc_number"
    ],
    "📚 Course Details": [
        "course_department","medium_of_instruction","admission_category"
    ],
    "🏦 Bank Details": [
        "bank_account_number","ifsc_code","bank_name"
    ],
    "🔖 Other Details": [
        "hostel_required","transport_required","scholarship_details",
        "emergency_contact_name","emergency_contact_number"
    ],
}

GENDER_OPTIONS    = ["", "Male", "Female", "Other", "Transgender"]
BLOOD_OPTIONS     = ["", "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
YES_NO            = ["", "Yes", "No"]
CATEGORY_OPTIONS  = ["", "General", "OBC", "SC", "ST", "Management", "NRI",
                     "Counseling", "Sports", "Other"]
MEDIUM_OPTIONS    = ["", "English", "Tamil", "Hindi", "Telugu", "Kannada",
                     "Malayalam", "Other"]


def render_results(valid, errs):
    st.markdown(f"""
    <div class="stat-row">
      <div class="stat-card"><div class="num">{len(valid)}</div><div class="lbl">Valid Records</div></div>
      <div class="stat-card"><div class="num" style="color:#ef5350">{len(errs)}</div><div class="lbl">Errors</div></div>
      <div class="stat-card"><div class="num" style="color:#66bb6a">{len(valid)}</div><div class="lbl">Ready to Export</div></div>
    </div>
    """, unsafe_allow_html=True)

    rt1, rt2 = st.tabs([f"✅ Valid Records ({len(valid)})", f"⚠️ Errors ({len(errs)})"])
    with rt1:
        if valid:
            df_v = pd.DataFrame(valid).rename(columns=FIELD_LABELS)
            df_v.index += 1
            st.dataframe(df_v, use_container_width=True, height=340)
            st.download_button("⬇️ Download as CSV",
                               df_v.to_csv(index=False).encode(),
                               "extracted_students.csv", "text/csv")
        else:
            st.info("No valid records extracted.")
    with rt2:
        if errs:
            df_e = pd.DataFrame(errs)
            df_e.index += 1
            st.dataframe(df_e, use_container_width=True, height=280)
        else:
            st.success("No validation errors — all records are clean!")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 1 — Process Forms
# ═════════════════════════════════════════════════════════════════════════════
if page == "📤 Process Forms":

    tab_upload, tab_manual = st.tabs(["📂 Upload File", "✏️ Manual Entry"])

    # ── Upload tab ────────────────────────────────────────────────────────────
    with tab_upload:
        st.markdown('<div class="section-title">Upload Admission Form</div>',
                    unsafe_allow_html=True)
        st.markdown("""
        <div class="upload-hint">
          <span style="font-size:2rem">📎</span><br>
          Drag & drop your admission form here<br>
          <small><b>PDF · DOCX · CSV · XLSX</b> &nbsp;|&nbsp; Max 200 MB</small>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Choose file", type=["csv","xlsx","xls","pdf","docx","doc"],
            label_visibility="collapsed")

        if uploaded_file:
            ext = uploaded_file.name.split(".")[-1].upper()
            size_kb = len(uploaded_file.getvalue()) / 1024
            c1, c2, c3 = st.columns([4, 1, 1])
            c1.markdown(f"**📄 {uploaded_file.name}**")
            c2.markdown(f"`{ext}`")
            c3.caption(f"{size_kb:.1f} KB")

            if ext in ("PDF", "DOCX", "DOC"):
                st.markdown("""
                <div class="info-box">
                  📌 <b>Unstructured document detected.</b> The system scans for labelled fields
                  like <i>Name:</i>, <i>Reg No:</i>, <i>Email:</i>, <i>Father's Name:</i>, etc.
                  Ensure labels are clearly written for best extraction accuracy.
                </div>
                """, unsafe_allow_html=True)

            if st.button("⚙️ Process Form", type="primary"):
                with st.spinner("Extracting and validating…"):
                    try:
                        resp = requests.post(f"{API_URL}/process-form/",
                                             files={"file": (uploaded_file.name,
                                                             uploaded_file.getvalue())})
                        if resp.status_code == 200:
                            result = resp.json()
                            if result.get("status") == "error":
                                st.error(f"❌ {result['message']}")
                            else:
                                st.session_state.valid_data = result.get("valid_data") or []
                                st.session_state.errors    = result.get("errors") or []
                                st.session_state.processed = True
                        else:
                            st.error(f"Server error {resp.status_code}: {resp.text}")
                    except requests.exceptions.ConnectionError:
                        st.error("Cannot reach backend. Make sure FastAPI is running on port 8000.")

        if st.session_state.processed:
            render_results(st.session_state.valid_data or [],
                           st.session_state.errors or [])

    # ── Manual Entry tab ──────────────────────────────────────────────────────
    with tab_manual:
        st.markdown('<div class="section-title">Add a Student Record Manually</div>',
                    unsafe_allow_html=True)

        with st.form("manual_form", clear_on_submit=True):

            # ── Personal Details ──────────────────────────────────────────────
            st.markdown("#### 👤 Personal Details")
            c1, c2, c3 = st.columns(3)
            name          = c1.text_input("Full Name *", placeholder="Arjun Sharma")
            dob           = c2.text_input("Date of Birth", placeholder="DD/MM/YYYY")
            gender        = c3.selectbox("Gender", GENDER_OPTIONS)

            c4, c5, c6 = st.columns(3)
            blood_group   = c4.selectbox("Blood Group", BLOOD_OPTIONS)
            aadhaar       = c5.text_input("Aadhaar Number", placeholder="XXXX XXXX XXXX")
            nationality   = c6.text_input("Nationality", placeholder="Indian")

            c7, c8, c9 = st.columns(3)
            religion      = c7.text_input("Religion")
            community     = c8.text_input("Community")
            caste         = c9.text_input("Caste")

            st.markdown("---")
            # ── Contact Details ───────────────────────────────────────────────
            st.markdown("#### 📞 Contact Details")
            c1, c2 = st.columns(2)
            mobile        = c1.text_input("Mobile Number *", placeholder="+91 9XXXXXXXXX")
            email         = c2.text_input("Email ID *", placeholder="student@college.edu")
            address       = st.text_area("Residential Address", height=80)
            parent_mobile = st.text_input("Parent's Contact Number")

            st.markdown("---")
            # ── Parent / Guardian ─────────────────────────────────────────────
            st.markdown("#### 👨‍👩‍👧 Parent / Guardian Details")
            c1, c2 = st.columns(2)
            father_name   = c1.text_input("Father's Name")
            father_occ    = c2.text_input("Father's Occupation")
            c3, c4 = st.columns(2)
            mother_name   = c3.text_input("Mother's Name")
            mother_occ    = c4.text_input("Mother's Occupation")
            c5, c6, c7 = st.columns(3)
            annual_income = c5.text_input("Annual Income", placeholder="e.g. 3,00,000")
            guardian_name = c6.text_input("Guardian Name (if applicable)")
            guardian_rel  = c7.text_input("Guardian Relation")

            st.markdown("---")
            # ── Academic Details ──────────────────────────────────────────────
            st.markdown("#### 🎓 Academic Details")
            c1, c2 = st.columns(2)
            reg_number    = c1.text_input("Registration Number", placeholder="REG2024001")
            prev_school   = c2.text_input("Previous School / College")
            c3, c4, c5 = st.columns(3)
            board_univ    = c3.text_input("Board / University")
            marks         = c4.text_input("Marks / % / CGPA", placeholder="85% or 8.5")
            year_pass     = c5.text_input("Year of Passing", placeholder="2024")
            tc_number     = st.text_input("Transfer Certificate (TC) Number")

            st.markdown("---")
            # ── Course Details ────────────────────────────────────────────────
            st.markdown("#### 📚 Course Details")
            c1, c2, c3 = st.columns(3)
            course_dept   = c1.text_input("Course / Department", placeholder="B.E. Computer Science")
            medium        = c2.selectbox("Medium of Instruction", MEDIUM_OPTIONS)
            adm_category  = c3.selectbox("Admission Category", CATEGORY_OPTIONS)

            st.markdown("---")
            # ── Bank Details ──────────────────────────────────────────────────
            st.markdown("#### 🏦 Bank Details")
            c1, c2, c3 = st.columns(3)
            bank_acc      = c1.text_input("Bank Account Number")
            ifsc          = c2.text_input("IFSC Code", placeholder="SBIN0001234")
            bank_name     = c3.text_input("Bank Name")

            st.markdown("---")
            # ── Other Details ─────────────────────────────────────────────────
            st.markdown("#### 🔖 Other Details")
            c1, c2 = st.columns(2)
            hostel        = c1.selectbox("Hostel Required", YES_NO)
            transport     = c2.selectbox("Transport Required", YES_NO)
            scholarship   = st.text_input("Scholarship Details")
            c3, c4 = st.columns(2)
            emg_name      = c3.text_input("Emergency Contact Name")
            emg_number    = c4.text_input("Emergency Contact Number")

            st.markdown("---")
            submitted = st.form_submit_button("➕ Add Record", type="primary",
                                              use_container_width=True)

        if submitted:
            if not name:
                st.error("Full Name is required.")
            else:
                record = {
                    "name": name,
                    "date_of_birth": dob or None,
                    "gender": gender or None,
                    "blood_group": blood_group or None,
                    "aadhaar_number": aadhaar or None,
                    "nationality": nationality or None,
                    "religion": religion or None,
                    "community": community or None,
                    "caste": caste or None,
                    "mobile_number": mobile or None,
                    "email": email or None,
                    "residential_address": address or None,
                    "parent_contact_number": parent_mobile or None,
                    "father_name": father_name or None,
                    "father_occupation": father_occ or None,
                    "mother_name": mother_name or None,
                    "mother_occupation": mother_occ or None,
                    "annual_income": annual_income or None,
                    "guardian_name": guardian_name or None,
                    "guardian_relation": guardian_rel or None,
                    "registration_number": reg_number or None,
                    "previous_school": prev_school or None,
                    "board_university": board_univ or None,
                    "marks_percentage": marks or None,
                    "year_of_passing": year_pass or None,
                    "tc_number": tc_number or None,
                    "course_department": course_dept or None,
                    "medium_of_instruction": medium or None,
                    "admission_category": adm_category or None,
                    "bank_account_number": bank_acc or None,
                    "ifsc_code": ifsc or None,
                    "bank_name": bank_name or None,
                    "hostel_required": hostel or None,
                    "transport_required": transport or None,
                    "scholarship_details": scholarship or None,
                    "emergency_contact_name": emg_name or None,
                    "emergency_contact_number": emg_number or None,
                }
                # Remove None values
                record = {k: v for k, v in record.items() if v}
                if st.session_state.valid_data is None:
                    st.session_state.valid_data = []
                st.session_state.valid_data.append(record)
                st.session_state.processed = True
                st.success(f"✅ Record for **{name}** added to the queue.")

        if st.session_state.valid_data:
            st.markdown("**Records in Queue**")
            df_q = pd.DataFrame(st.session_state.valid_data).rename(columns=FIELD_LABELS)
            df_q.index += 1
            st.dataframe(df_q, use_container_width=True)

    # ── Export section ────────────────────────────────────────────────────────
    if st.session_state.valid_data:
        st.markdown("---")
        st.markdown("### 🚀 Export to Database")
        c1, c2, c3 = st.columns([3, 1, 1])
        c1.markdown(f"**{len(st.session_state.valid_data)} record(s)** ready to export.")
        export_btn = c2.button("🚀 Export", type="primary", use_container_width=True)
        clear_btn  = c3.button("🗑️ Clear", use_container_width=True)

        if clear_btn:
            st.session_state.valid_data = None
            st.session_state.processed  = False
            st.session_state.errors     = []
            st.rerun()

        if export_btn:
            with st.spinner("Saving…"):
                try:
                    resp = requests.post(f"{API_URL}/export/",
                                         json=st.session_state.valid_data)
                    if resp.status_code == 200:
                        r = resp.json()
                        st.session_state.last_export = r
                        st.session_state.valid_data  = None
                        st.session_state.processed   = False
                        st.rerun()
                    else:
                        st.error(f"Export failed: {resp.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot reach backend.")

    if st.session_state.last_export:
        e = st.session_state.last_export
        st.success(
            f"✅ Export complete — **{e.get('exported',0)}** saved, "
            f"**{e.get('skipped_duplicates',0)}** duplicate(s) skipped."
        )
        st.session_state.last_export = None


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 2 — View Database
# ═════════════════════════════════════════════════════════════════════════════
elif page == "🗄️ View Database":
    st.markdown("## 🗄️ Student Database")

    # init delete confirmation state
    if "confirm_delete_id" not in st.session_state:
        st.session_state.confirm_delete_id = None

    try:
        resp = requests.get(f"{API_URL}/students", timeout=5)
        if resp.status_code == 200:
            students = resp.json()
            if not students:
                st.info("No records yet. Process and export some forms first.")
            else:
                df_full = pd.DataFrame(students)

                search = st.text_input("🔍 Search by any field", "")
                if search:
                    mask = df_full.apply(
                        lambda col: col.astype(str).str.contains(search, case=False)
                    ).any(axis=1)
                    df_full = df_full[mask]

                st.markdown(f"""
                <div class="stat-row">
                  <div class="stat-card"><div class="num">{len(students)}</div><div class="lbl">Total</div></div>
                  <div class="stat-card"><div class="num">{len(df_full)}</div><div class="lbl">Showing</div></div>
                </div>
                """, unsafe_allow_html=True)

                # ── Per-row delete buttons ────────────────────────────────────
                st.markdown('<div class="section-title">Records</div>', unsafe_allow_html=True)

                # Table header
                hcols = st.columns([0.5, 2.5, 2, 1.5, 1.5, 1])
                hcols[0].markdown("**#**")
                hcols[1].markdown("**Full Name**")
                hcols[2].markdown("**Email**")
                hcols[3].markdown("**Reg Number**")
                hcols[4].markdown("**Mobile**")
                hcols[5].markdown("**Action**")
                st.markdown("<hr style='margin:4px 0 8px;border-color:#2a2f3e'>",
                            unsafe_allow_html=True)

                for i, row in df_full.iterrows():
                    student_id = row.get("id", i)
                    rcols = st.columns([0.5, 2.5, 2, 1.5, 1.5, 1])
                    rcols[0].markdown(f"{i + 1}")
                    rcols[1].markdown(str(row.get("name", "—")))
                    rcols[2].markdown(str(row.get("email") or "—"))
                    rcols[3].markdown(str(row.get("registration_number") or "—"))
                    rcols[4].markdown(str(row.get("mobile_number") or "—"))

                    # Delete button
                    if rcols[5].button("🗑️", key=f"del_{student_id}_{i}",
                                       help="Delete this record"):
                        st.session_state.confirm_delete_id = student_id
                        st.rerun()

                # ── Confirmation dialog ───────────────────────────────────────
                if st.session_state.confirm_delete_id is not None:
                    del_id = st.session_state.confirm_delete_id
                    # Find the student name for display
                    match = df_full[df_full["id"] == del_id]
                    del_name = match["name"].values[0] if not match.empty else f"ID {del_id}"

                    st.warning(f"⚠️ Are you sure you want to delete **{del_name}**? This cannot be undone.")
                    c1, c2, _ = st.columns([1, 1, 4])
                    if c1.button("✅ Yes, Delete", type="primary"):
                        try:
                            r = requests.delete(f"{API_URL}/students/{del_id}", timeout=5)
                            if r.status_code == 200:
                                st.success(f"Deleted **{del_name}** successfully.")
                            else:
                                st.error(f"Failed to delete: {r.text}")
                        except Exception as e:
                            st.error(f"Error: {e}")
                        st.session_state.confirm_delete_id = None
                        st.rerun()
                    if c2.button("❌ Cancel"):
                        st.session_state.confirm_delete_id = None
                        st.rerun()

                st.markdown("---")

                # ── Section tabs for full details ─────────────────────────────
                st.markdown("**Full Details by Section**")
                display_df = df_full.rename(columns=FIELD_LABELS)
                sec_tabs = st.tabs(list(SECTIONS.keys()))
                for tab, (sec_name, fields) in zip(sec_tabs, SECTIONS.items()):
                    with tab:
                        cols_present = [FIELD_LABELS[f] for f in fields
                                        if FIELD_LABELS[f] in display_df.columns]
                        if cols_present:
                            st.dataframe(display_df[cols_present],
                                         use_container_width=True, height=320)
                        else:
                            st.info("No data for this section.")

                st.download_button(
                    "⬇️ Download Full Database as CSV",
                    df_full.rename(columns=FIELD_LABELS).to_csv(index=False).encode(),
                    "student_database.csv", "text/csv"
                )
        else:
            st.error(f"Failed to fetch: {resp.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("Cannot reach backend.")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 3 — Help
# ═════════════════════════════════════════════════════════════════════════════
elif page == "ℹ️ Help":
    st.markdown("## ℹ️ How to Use")

    with st.expander("📄 PDF / DOCX Upload", expanded=True):
        st.markdown("""
The system scans the document for **labelled fields**. Use clear labels like:

| Field | Accepted Labels |
|-------|----------------|
| Name | `Name:`, `Full Name:`, `Student Name:` |
| Registration | `Reg No:`, `Registration Number:`, `Roll No:` |
| Email | Any valid email address |
| Date of Birth | `DOB:`, `Date of Birth:` |
| Father's Name | `Father's Name:`, `Father Name:` |
| Mobile | `Mobile:`, `Phone:`, `Contact No:` |
| Aadhaar | `Aadhaar:`, `Aadhaar Number:` |
| Blood Group | `Blood Group:` followed by A+/B- etc. |
| Hostel | `Hostel Required: Yes/No` |

> **Tip:** PDFs must have selectable text (not scanned images without OCR).
        """)

    with st.expander("📊 CSV / Excel Upload"):
        st.markdown("""
Your file can use any of these column names (case-insensitive):

| Section | Accepted Column Names |
|---------|----------------------|
| Personal | `Name`, `Full Name`, `DOB`, `Date of Birth`, `Gender`, `Blood Group`, `Aadhaar`, `Nationality`, `Religion`, `Community`, `Caste` |
| Contact | `Mobile`, `Email`, `Address`, `Residential Address`, `Parent Contact` |
| Parent | `Father Name`, `Father's Name`, `Father Occupation`, `Mother Name`, `Mother Occupation`, `Annual Income`, `Guardian Name` |
| Academic | `RegNo`, `Reg No`, `Registration Number`, `Previous School`, `Board`, `University`, `Marks`, `Percentage`, `CGPA`, `Year of Passing`, `TC Number` |
| Course | `Course`, `Department`, `Medium`, `Admission Category`, `Category` |
| Bank | `Account Number`, `IFSC`, `IFSC Code`, `Bank Name` |
| Other | `Hostel`, `Transport`, `Scholarship`, `Emergency Contact`, `Emergency Contact Number` |
        """)

    with st.expander("✏️ Manual Entry"):
        st.markdown("""
- Fill in as many fields as available — only **Full Name** is required.
- Records are queued and exported to the database in bulk.
- Use dropdowns for Gender, Blood Group, Hostel, Transport, and Category.
        """)

    with st.expander("🗄️ Database"):
        st.markdown("""
- Records are stored in `backend/admission_db.sqlite`.
- Duplicates (same Registration Number, Email, or Aadhaar) are automatically skipped.
- Use **View Database** to browse by section, search, and download.
        """)
