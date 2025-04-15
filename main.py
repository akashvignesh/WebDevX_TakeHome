import os
from fastapi import FastAPI, UploadFile, Form, Depends, HTTPException, status, File
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Lead, LeadStatus
from schemas import LeadOut
from email_utils import send_email
import shutil
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
Base.metadata.create_all(bind=engine)

security = HTTPBasic()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != os.getenv("BASIC_AUTH_USER") or credentials.password != os.getenv("BASIC_AUTH_PASS"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

@app.post("/leads", response_model=LeadOut)
async def create_lead(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    path = f"{UPLOAD_DIR}/{resume.filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(resume.file, f)

    lead = Lead(first_name=first_name, last_name=last_name, email=email, resume_path=path)
    db.add(lead)
    db.commit()
    db.refresh(lead)

    await send_email(email, "Thank you", f"Hi {first_name}, thanks for submitting your info.")

    with open(path, "rb") as file_data:
        await send_email(
            os.getenv("ATTORNEY_EMAIL"),
            "New Lead Submitted",
            f"New lead: {first_name} {last_name}, {email}",
            attachment=file_data.read(),
            filename=resume.filename
        )

    return lead

@app.get("/leads", response_model=list[LeadOut])
def list_leads(db: Session = Depends(get_db), _: bool = Depends(authenticate)):
    return db.query(Lead).all()

@app.post("/leads/{lead_id}/mark-reached", response_model=LeadOut)
def mark_lead(lead_id: int, db: Session = Depends(get_db), _: bool = Depends(authenticate)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    lead.status = LeadStatus.REACHED_OUT
    db.commit()
    db.refresh(lead)
    return lead
@app.get("/")
def home():
    return {"message": "Welcome to the Leads Management API!"}