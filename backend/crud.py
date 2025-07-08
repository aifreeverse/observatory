
from sqlalchemy.orm import Session
from . import database as models, schemas

def get_content_gaps(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.ContentGap).offset(skip).limit(limit).all()

def create_content_gap(db: Session, gap: schemas.ContentGapCreate):
    db_gap = models.ContentGap(**gap.dict())
    db.add(db_gap)
    db.commit()
    db.refresh(db_gap)
    return db_gap
