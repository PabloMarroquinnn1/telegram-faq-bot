from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.database import get_db
from app.models.models import Question, Category
from app.routes.auth import get_current_user

router = APIRouter()

# --- Schemas ---
class QuestionCreate(BaseModel):
    question_text: str
    answer_text: str
    category_id: Optional[int] = None

class QuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    answer_text: Optional[str] = None
    category_id: Optional[int] = None

class QuestionResponse(BaseModel):
    id: int
    question_text: str
    answer_text: str
    category_id: Optional[int] = None
    category_name: Optional[str] = None

    class Config:
        from_attributes = True

# --- Endpoints ---
@router.get("/", response_model=List[QuestionResponse])
def get_questions(db: Session = Depends(get_db)):
    questions = db.query(Question).all()
    result = []
    for q in questions:
        result.append(QuestionResponse(
            id=q.id,
            question_text=q.question_text,
            answer_text=q.answer_text,
            category_id=q.category_id,
            category_name=q.category.name if q.category else None
        ))
    return result

@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    return QuestionResponse(
        id=q.id,
        question_text=q.question_text,
        answer_text=q.answer_text,
        category_id=q.category_id,
        category_name=q.category.name if q.category else None
    )

@router.post("/", response_model=QuestionResponse)
def create_question(data: QuestionCreate, db: Session = Depends(get_db), 
                    current_user=Depends(get_current_user)):
    q = Question(**data.model_dump())
    db.add(q)
    db.commit()
    db.refresh(q)
    return QuestionResponse(
        id=q.id,
        question_text=q.question_text,
        answer_text=q.answer_text,
        category_id=q.category_id,
        category_name=q.category.name if q.category else None
    )

@router.put("/{question_id}", response_model=QuestionResponse)
def update_question(question_id: int, data: QuestionUpdate, 
                    db: Session = Depends(get_db),
                    current_user=Depends(get_current_user)):
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(q, key, value)
    db.commit()
    db.refresh(q)
    return QuestionResponse(
        id=q.id,
        question_text=q.question_text,
        answer_text=q.answer_text,
        category_id=q.category_id,
        category_name=q.category.name if q.category else None
    )

@router.delete("/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db),
                    current_user=Depends(get_current_user)):
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    db.delete(q)
    db.commit()
    return {"message": "Pregunta eliminada correctamente"}

@router.get("/search/query")
def search_question(q: str, db: Session = Depends(get_db)):
    """Endpoint que usa el bot para buscar respuestas"""
    questions = db.query(Question).all()
    q_lower = q.lower()
    for question in questions:
        if q_lower in question.question_text.lower():
            return {
                "found": True,
                "answer": question.answer_text,
                "question": question.question_text
            }
    return {"found": False, "answer": None}