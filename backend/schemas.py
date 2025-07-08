
from pydantic import BaseModel

class ContentGapBase(BaseModel):
    title: str
    demand_score: float
    sources: str

class ContentGapCreate(ContentGapBase):
    pass

class ContentGap(ContentGapBase):
    id: int

    class Config:
        orm_mode = True
