# app/api/v1/dashboard.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import List, Dict
from app.db.session import get_db
from app.models import models

router = APIRouter()

@router.get("/stats/active-users")
def get_active_users(db: Session = Depends(get_db)):
    """최근 1개월 내 접속 + 프로젝트 생성 1회 이상한 유저 수 조회"""
    one_month_ago = datetime.utcnow() - timedelta(days=30)
    
    # 최근 1개월 내 접속한 유저
    recent_login_users = db.query(models.User.id).filter(
        models.User.last_login >= one_month_ago
    ).subquery()
    
    # 최근 1개월 내 프로젝트 생성한 유저
    project_created_users = db.query(models.User.id).filter(
        and_(
            models.Project.created_at >= one_month_ago,
            models.Project.is_active == True
        )
    ).join(models.Project).subquery()
    
    # 교집합 계산
    active_users = db.query(func.count(recent_login_users.c.id)).filter(
        recent_login_users.c.id.in_(
            db.query(project_created_users.c.id)
        )
    ).scalar()
    
    return {"active_users_count": active_users}

@router.get("/stats/daily")
def get_daily_stats(date: str = None, db: Session = Depends(get_db)):
    """일별 주요 지표 조회"""
    if date is None:
        date = datetime.utcnow().date()
    else:
        date = datetime.strptime(date, "%Y-%m-%d").date()
    
    next_date = date + timedelta(days=1)
    
    # 프로젝트 통계
    new_projects = db.query(func.count(models.Project.id)).filter(
        and_(
            models.Project.created_at >= date,
            models.Project.created_at < next_date
        )
    ).scalar()
    
    total_projects = db.query(func.count(models.Project.id)).scalar()
    
    # 결제 통계
    new_payments = db.query(
        func.count(models.Payment.id),
        func.sum(models.Payment.amount)
    ).filter(
        and_(
            models.Payment.created_at >= date,
            models.Payment.created_at < next_date
        )
    ).first()
    
    total_payments = db.query(
        func.count(models.Payment.id),
        func.sum(models.Payment.amount)
    ).first()
    
    # 회원가입 통계
    new_users = db.query(func.count(models.User.id)).filter(
        and_(
            models.User.created_at >= date,
            models.User.created_at < next_date
        )
    ).scalar()
    
    total_users = db.query(func.count(models.User.id)).scalar()
    
    return {
        "date": str(date),
        "projects": {
            "new": new_projects,
            "total": total_projects
        },
        "payments": {
            "new_count": new_payments[0] or 0,
            "new_amount": float(new_payments[1] or 0),
            "total_count": total_payments[0] or 0,
            "total_amount": float(total_payments[1] or 0)
        },
        "users": {
            "new": new_users,
            "total": total_users
        }
    }