from sqlalchemy import Column, Integer, String, Enum
from database import Base
import enum

class LeadStatus(str, enum.Enum):
    PENDING = "PENDING"
    REACHED_OUT = "REACHED_OUT"

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    resume_path = Column(String, nullable=False)
    status = Column(Enum(LeadStatus), default=LeadStatus.PENDING)
