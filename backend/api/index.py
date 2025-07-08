
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import SessionLocal, create_db_and_tables

# Create database tables
create_db_and_tables()

app = FastAPI()

# CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Vercel deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api")
def read_root():
    return {"message": "Observatory Backend is running"}

@app.get("/api/content-gaps", response_model=list[schemas.ContentGap])
def get_content_gaps(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    gaps = crud.get_content_gaps(db, skip=skip, limit=limit)
    if not gaps:
        return []
    return gaps
