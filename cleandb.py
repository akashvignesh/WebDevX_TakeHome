from database import SessionLocal
from models import Lead

db = SessionLocal()

# Track deleted records
deleted_invalid = 0
deleted_duplicates = 0

# Step 1: Remove leads with invalid emails (missing "@")
leads = db.query(Lead).all()
valid_leads = []

for lead in leads:
    if "@" not in lead.email:
        print(f"Deleting invalid lead: {lead.id}, {lead.email}")
        db.delete(lead)
        deleted_invalid += 1
    else:
        valid_leads.append(lead)

# Step 2: Remove duplicate leads (keep first occurrence)
unique_keys = set()
for lead in valid_leads:
    key = (lead.first_name.lower(), lead.last_name.lower(), lead.email.lower())
    if key in unique_keys:
        print(f"Deleting duplicate lead: {lead.id}, {lead.email}")
        db.delete(lead)
        deleted_duplicates += 1
    else:
        unique_keys.add(key)

# Finalize changes
db.commit()
db.close()

print(f"\nCleanup complete.")
print(f"Deleted {deleted_invalid} invalid leads.")
print(f"Deleted {deleted_duplicates} duplicate leads.")
