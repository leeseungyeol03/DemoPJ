# routers/feedback.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models import Feedback
from schemas import FeedbackCreate, FeedbackOut
from sqlalchemy.future import select

router = APIRouter()

@router.post("/submit", response_model=FeedbackOut)
async def submit_feedback(payload: FeedbackCreate, db: AsyncSession = Depends(get_session)):
    fb = Feedback(**payload.dict())
    db.add(fb)
    await db.commit()
    await db.refresh(fb)
    return fb

@router.get("/admin/feedbacks", response_model=list[FeedbackOut])
async def get_all_feedbacks(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Feedback).order_by(Feedback.created_at.desc()))
    return result.scalars().all()
