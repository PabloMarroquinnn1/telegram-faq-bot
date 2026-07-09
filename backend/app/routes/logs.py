from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.database import get_db
from app.models.models import QueryLog
from app.routes.auth import get_current_user

router = APIRouter()

class LogCreate(BaseModel):
    telegram_user: Optional[str] = None
    query_text: str
    response_text: Optional[str] = None

class LogResponse(BaseModel):
    id: int
    telegram_user: Optional[str] = None
    query_text: str
    response_text: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

@router.get("/", response_model=List[LogResponse])
def get_logs(db: Session = Depends(get_db),
             current_user=Depends(get_current_user)):
    return db.query(QueryLog).order_by(QueryLog.created_at.desc()).all()

@router.post("/")
def create_log(data: LogCreate, db: Session = Depends(get_db)):
    log = QueryLog(**data.model_dump())
    db.add(log)
    db.commit()
    return {"message": "Log registrado"}

@router.get("/stats/summary")
def get_stats(db: Session = Depends(get_db),
              current_user=Depends(get_current_user)):
    total = db.query(QueryLog).count()
    from sqlalchemy import func
    top_queries = (
        db.query(QueryLog.query_text, func.count(QueryLog.query_text).label("count"))
        .group_by(QueryLog.query_text)
        .order_by(func.count(QueryLog.query_text).desc())
        .limit(5)
        .all()
    )
    return {
        "total_queries": total,
        "top_queries": [{"query": q, "count": c} for q, c in top_queries]
    }