# Lead Management Application (FastAPI + SQLite)

This is a lightweight lead management system built with **FastAPI** that supports:

- Public API for prospects to submit leads (with resume)
- Email notifications to both the prospect and internal attorney
- SQLite database for persistence
- Admin-only APIs protected by Basic Auth
- Ability to mark leads as "REACHED_OUT"
- Resume file upload and storage

---

## Features

Submit leads with:

- First Name
- Last Name
- Email
- Resume (file upload)

Sends email to:

- Prospect (confirmation)
- Internal attorney (with resume attached)

Admin capabilities:

- View all leads (`/leads`)
- Mark lead as REACHED_OUT (`/leads/{id}/mark-reached`)

---

## Tech Stack

- **Python 3.12+**
- **FastAPI**
- **SQLite + SQLAlchemy**
- **Nodemailer-compatible with Gmail (via aiosmtplib)**
- **Postman / Swagger UI for testing**

---

## Folder Structure

```
lead_app_fastapi/
├── main.py
├── models.py
├── schemas.py
├── database.py
├── email_utils.py
├── clean_leads.py
├── uploads/              # Resume file storage
├── leads.db              # SQLite database
├── .env                  # Email credentials & auth
└── README.md
```

---

## Setup Instructions

### 1. Clone and Install

```bash
git clone <repo-url>
cd lead_app_fastapi
python -m venv venv
source venv/bin/activate     # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

> If `requirements.txt` doesn't exist, install manually:

```bash
pip install fastapi uvicorn sqlalchemy aiosmtplib python-multipart python-dotenv
```

---

### 2. Configure `.env`

Create a `.env` file:

```env
EMAIL_USER=your_gmail@gmail.com
EMAIL_PASS=your_app_password        # Use a Gmail App Password
ATTORNEY_EMAIL=attorney@example.com # Change to a real email
BASIC_AUTH_USER=admin
BASIC_AUTH_PASS=secret123
```

---

### 3. Run the App

```bash
uvicorn main:app --reload
```

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## API Testing (Postman or Swagger)

### `POST /leads`

- **Type**: `form-data`
- Fields: `first_name`, `last_name`, `email`, `resume (file)`
- Public

### `GET /leads`

- Basic Auth protected (`admin:secret123`)
- Returns all leads

### `POST /leads/{id}/mark-reached`

- Basic Auth protected
- Marks the status as `REACHED_OUT`

---

## Clean Script

Run this to remove:

- Invalid email leads (missing `@`)
- Duplicate leads based on name + email

```bash
python clean_leads.py
```

---

## Requirements

```
fastapi
uvicorn
sqlalchemy
aiosmtplib
python-multipart
python-dotenv
```

You can export it with:

```bash
pip freeze > requirements.txt
```

---

## Status

- [x] SQLite database integration
- [x] Resume file handling
- [x] Email sending (Gmail App Password)
- [x] Admin authentication
- [x] Lead status tracking
- [x] Duplicate cleanup

---

## Contact

Feel free to reach out via issues or contributions!
