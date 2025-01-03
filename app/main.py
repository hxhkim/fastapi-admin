# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 이 import 추가
from app.core.config import settings

# FastAPI 앱 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 origin 허용. 실제 운영에서는 구체적인 도메인 지정 권장
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Admin"}