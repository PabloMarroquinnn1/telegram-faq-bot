from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.models.models import BotConfig
from app.routes.auth import get_current_user

router = APIRouter()

class ConfigUpdate(BaseModel):
    chat_id: Optional[str] = None

@router.get("/")
def get_config(db: Session = Depends(get_db),
               current_user=Depends(get_current_user)):
    config = db.query(BotConfig).first()
    if not config:
        return {"chat_id": None}
    return {"chat_id": config.chat_id}

@router.put("/")
def update_config(data: ConfigUpdate, db: Session = Depends(get_db),
                  current_user=Depends(get_current_user)):
    config = db.query(BotConfig).first()
    if not config:
        config = BotConfig(chat_id=data.chat_id)
        db.add(config)
    else:
        config.chat_id = data.chat_id
    db.commit()
    return {"message": "Configuración actualizada", "chat_id": data.chat_id}