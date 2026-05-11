# Admission Form Processor

A simple full-stack web application to upload admission forms, extract details, validate data, and export to PostgreSQL.

## Tech Stack
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Database**: PostgreSQL
- **Data Processing**: Pandas

## Getting Started

### 1. Database Setup
Make sure you have PostgreSQL running locally or via Docker. Create a database named `admission_db` with username `postgres` and password `postgres` (or update `backend/database.py` with your credentials).

### 2. Backend Setup
Open a terminal in the root directory and run:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
The backend will run at `http://localhost:8000`.

### 3. Frontend Setup
Open a new terminal window and run:
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```
The Streamlit interface will open in your browser.

### 4. Usage
- Go to the Streamlit app.
- Upload `sample_forms/sample_students.csv`.
- Click "Process Form" to see the extracted valid data and the validation errors.
- Click "Export to Database" to insert the valid records into your PostgreSQL database.
