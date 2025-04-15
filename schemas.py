from pydantic import BaseModel, EmailStr

class LeadOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    resume_path: str
    status: str

    class Config:
        orm_mode = True
